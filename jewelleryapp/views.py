from rest_framework import generics
from django.shortcuts import render,  get_object_or_404
from .models import *
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from rest_framework.exceptions import NotFound
from django.conf import settings
from rest_framework.generics import ListAPIView
from urllib.parse import urljoin
from rest_framework.parsers import MultiPartParser, FormParser
from cloudinary.uploader import upload
import requests
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated  
# from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.views import View
import random
from django.http import Http404
from .serializers import *
import cloudinary
import cloudinary.uploader
from rest_framework.filters import BaseFilterBackend
from rest_framework import status, permissions
import json
from rest_framework import generics
from rest_framework.views import APIView

from rest_framework import status
from rest_framework.permissions import AllowAny
from django.db.models import Count
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from twilio.rest import Client
from .models import Category, Product, UserVisit, SearchGif
# from .serializers import CategoryNameSerializer, PopularProductSerializer, SearchGifSerializer

from .utils import send_otp_via_sms
from rest_framework import permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import parsers

from jewelleryapp.models import PhoneOTP
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from jewelleryapp.auth.admin_authentication import AdminJWTAuthentication
from urllib.parse import quote_plus
from .authentication import CombinedJWTAuthentication

def index(request):
    return render(request, 'index.html')

class BaseListCreateAPIView(APIView):
    model = None
    serializer_class = None

    def get(self, request):
        items = self.model.objects.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        image = request.FILES.get('image')

        if image:
            cloudinary_response = cloudinary.uploader.upload(image)
            public_id = cloudinary_response.get('public_id')
            if public_id:
                data['image'] = public_id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BaseDetailAPIView(APIView):
    model = None
    serializer_class = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        instance = self.get_object(pk)
        data = request.data.copy()
        image = request.FILES.get('image')

        if image:
            cloudinary_response = cloudinary.uploader.upload(image)
            public_id = cloudinary_response.get('public_id')
            if public_id:
                data['image'] = public_id

        serializer = self.serializer_class(instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductListCreateAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication,AdminJWTAuthentication] 

#     def get(self, request, *args, **kwargs):
#         user = request.user if request.user.is_authenticated else None

#         classic_qs = Product.objects.filter(is_classic=True)
#         other_qs   = Product.objects.filter(is_classic=False)

#         context = {'request': request}  # Enables access to request.user in serializer

#         classic_data = ProductSerializer(classic_qs, many=True, context=context).data
#         other_data   = ProductSerializer(other_qs, many=True, context=context).data

#         return Response({
#             "classic_products": classic_data,
#             "other_products": other_data
#         }, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         images     = request.FILES.getlist('images')
#         image_urls = []

#         try:
#             for image in images[:5]:
#                 res = uploader.upload(image)
#                 image_urls.append(res["secure_url"])
#         except Exception as e:
#             return Response({"error": f"Image upload failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         data = request.data.copy()
#         data['images'] = image_urls

#         if 'ar_model_glb' in request.FILES:
#             glb = uploader.upload(request.FILES['ar_model_glb'], resource_type='raw')
#             data['ar_model_glb'] = f"https://res.cloudinary.com/dvllntzo0/raw/upload/v{glb['version']}/{glb['public_id']}"

#         if 'ar_model_gltf' in request.FILES:
#             gltf = uploader.upload(request.FILES['ar_model_gltf'], resource_type='raw')
#             data['ar_model_gltf'] = gltf['secure_url']

#         serializer = ProductSerializer(data=data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductListCreateAPIView(APIView):
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        classic_qs = Product.objects.filter(is_classic=True)
        other_qs   = Product.objects.filter(is_classic=False)

        context = {'request': request}
        classic_data = ProductSerializer(classic_qs, many=True, context=context).data
        other_data   = ProductSerializer(other_qs, many=True, context=context).data

        return Response({
            "classic_products": classic_data,
            "other_products": other_data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        images     = request.FILES.getlist('images')
        image_urls = []

        try:
            for image in images[:5]:
                res = uploader.upload(image)
                image_urls.append(res["secure_url"])
        except Exception as e:
            return Response({"error": f"Image upload failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = request.data.copy()
        data['images'] = image_urls

        if 'ar_model_glb' in request.FILES:
            glb = uploader.upload(request.FILES['ar_model_glb'], resource_type='raw')
            data['ar_model_glb'] = f"https://res.cloudinary.com/YOUR_CLOUD_NAME/raw/upload/v{glb['version']}/{glb['public_id']}"

        if 'ar_model_gltf' in request.FILES:
            gltf = uploader.upload(request.FILES['ar_model_gltf'], resource_type='raw')
            data['ar_model_gltf'] = gltf['secure_url']

        serializer = ProductSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductDetailAPIView(APIView):
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound("Product not found")

    def get(self, request, pk, *args, **kwargs):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        product = self.get_object(pk)
        data = dict(request.data)

        # ✅ Handle multiple image uploads (up to 5)
        new_images = request.FILES.getlist('images')
        if new_images:
            uploaded_images = []
            try:
                for image in new_images[:5]:
                    upload_result = uploader.upload(image)
                    uploaded_images.append(upload_result["secure_url"])
                data['images'] = json.dumps(uploaded_images)
            except Exception as e:
                return Response({"error": f"Image upload failed: {str(e)}"}, status=500)
        else:
            data.pop('images', None)

        # ✅ Handle AR model GLB
        if 'ar_model_glb' in request.FILES:
            glb_upload = uploader.upload(request.FILES['ar_model_glb'], resource_type='raw')
            data['ar_model_glb'] = f"https://res.cloudinary.com/dvllntzo0/raw/upload/v{glb_upload['version']}/{glb_upload['public_id']}"

        # ✅ Handle AR model GLTF
        if 'ar_model_gltf' in request.FILES:
            gltf_upload = uploader.upload(request.FILES['ar_model_gltf'], resource_type='raw')
            data['ar_model_gltf'] = gltf_upload['secure_url']

        # ✅ Parse JSON string for 'images' if needed
        if 'images' in data and isinstance(data['images'], str):
            try:
                data['images'] = json.loads(data['images'])
            except json.JSONDecodeError:
                return Response({"images": ["Value must be valid JSON."]}, status=400)

        messages = []

        # ✅ Handle stock increment
        if 'total_stock' in data:
            try:
                stock_value = data['total_stock'][0] if isinstance(data['total_stock'], list) else data['total_stock']
                added_stock = int(stock_value)
                product.total_stock += added_stock
                product.save()
                messages.append(f"Added {added_stock} to stock.")
            except ValueError:
                return Response({"total_stock": ["A valid integer is required."]}, status=400)
            data.pop('total_stock')

        # ✅ Handle sold_count increment
        if 'sold_count' in data:
            try:
                sold_value = data['sold_count'][0] if isinstance(data['sold_count'], list) else data['sold_count']
                sold_increment = int(sold_value)
                if sold_increment < 0:
                    return Response({"sold_count": ["Sold count cannot be negative."]}, status=400)

                available_stock = product.total_stock - product.sold_count
                if sold_increment > available_stock:
                    return Response({
                        "message": "Not enough stock to sell.",
                        "product": ProductSerializer(product).data
                    }, status=400)

                product.sold_count += sold_increment
                product.save()
                messages.append(f"{sold_increment} items sold.")
            except ValueError:
                return Response({"sold_count": ["A valid integer is required."]}, status=400)
            data.pop('sold_count')

        # ✅ Save changes
        serializer = ProductSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": " ".join(messages) or "Product updated successfully.",
                "product": serializer.data
            })

        return Response(serializer.errors, status=400)



class ProductListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(is_classic=False)
        serializer = ProductSerializer(products, many=True)
        return Response({
            "products": serializer.data
        }, status=status.HTTP_200_OK)

class ClassicProductListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]  # Anyone can view, but we try to identify user if possible

    def get(self, request, *args, **kwargs):
        user = None

        # First try: authenticated user from Bearer token
        if request.user and request.user.is_authenticated:
            user = request.user

        # Fallback: optional user_id in query params
        elif 'user_id' in request.query_params:
            raw_user_id = request.query_params.get('user_id')
            try:
                user_uuid = UUID(raw_user_id)
                user = Register.objects.get(id=user_uuid)
            except (ValueError, Register.DoesNotExist):
                pass

        # Fetch all classic products
        products = Product.objects.filter(is_classic=True)
        serializer = ClassicProductListSerializer(products, many=True)
        products_data = serializer.data

        # Get wishlist product IDs for this user (if any)
        wishlist_product_ids = set()
        if user:
            wishlist_product_ids = set(
                Wishlist.objects.filter(user=user, product__is_classic=True)
                .values_list('product_id', flat=True)
            )

        # Attach detail URL and wishlist flag
        for product in products_data:
            pid = product["id"]
            product['detail_url'] = request.build_absolute_uri(f'/api/products/classic/{pid}/')
            product['wishlist'] = pid in wishlist_product_ids

        return Response({"classic_products": products_data}, status=status.HTTP_200_OK)


class ClassicProductDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk, is_classic=True)
        except Product.DoesNotExist:
            raise NotFound("Classic product not found")

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['is_classic'] = True

        new_images = request.FILES.getlist('images')
        if new_images:
            uploaded_images = []
            try:
                for image in new_images[:5]:
                    upload_result = uploader.upload(image)
                    uploaded_images.append(upload_result['secure_url'])
                data['images'] = uploaded_images
            except Exception as e:
                return Response({"error": f"Image upload failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if 'ar_model_glb' in request.FILES:
            glb_upload = uploader.upload(request.FILES['ar_model_glb'], resource_type='raw')
            version = glb_upload['version']
            public_id = glb_upload['public_id']
            cloud_name = 'dvllntzo0'
            data['ar_model_glb'] = f"https://res.cloudinary.com/{cloud_name}/raw/upload/v{version}/{public_id}"

        if 'ar_model_gltf' in request.FILES:
            gltf_upload = uploader.upload(request.FILES['ar_model_gltf'], resource_type='raw')
            data['ar_model_gltf'] = gltf_upload['secure_url']

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, *args, **kwargs):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        product = self.get_object(pk)
        data = request.data.copy()

        new_images = request.FILES.getlist('images')
        if new_images:
            uploaded_images = []
            try:
                for image in new_images[:5]:
                    upload_result = uploader.upload(image)
                    uploaded_images.append(upload_result['secure_url'])
                data['images'] = uploaded_images
            except Exception as e:
                return Response({"error": f"Image upload failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            data.pop('images', None)

        if 'ar_model_glb' in request.FILES:
            glb_upload = uploader.upload(request.FILES['ar_model_glb'], resource_type='raw')
            version = glb_upload['version']
            public_id = glb_upload['public_id']
            cloud_name = 'dvllntzo0'
            data['ar_model_glb'] = f"https://res.cloudinary.com/{cloud_name}/raw/upload/v{version}/{public_id}"

        if 'ar_model_gltf' in request.FILES:
            gltf_upload = uploader.upload(request.FILES['ar_model_gltf'], resource_type='raw')
            data['ar_model_gltf'] = gltf_upload['secure_url']

        serializer = ProductSerializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        product = self.get_object(pk)
        product.delete()
        return Response({"detail": "Classic product deleted."}, status=status.HTTP_204_NO_CONTENT)


    

# Material API
class MaterialListCreateAPIView(BaseListCreateAPIView):
    model = Material
    serializer_class = MaterialSerializer

class MaterialDetailAPIView(BaseDetailAPIView):
    model = Material
    serializer_class = MaterialSerializer



# class CategoryListCreateAPIView(APIView):
#     parser_classes = [MultiPartParser, FormParser]

#     # ✅ Handle GET request to list all categories
#     def get(self, request):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)

#     # ✅ Handle POST request to create a new category with subcategories
#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# class CategoryDetailAPIView(APIView):
#     parser_classes = [MultiPartParser, FormParser]

#     def get_object(self, pk):
#         return get_object_or_404(Category, pk=pk)

#     # ✅ Handle GET request for one category
#     def get(self, request, pk):
#         category = self.get_object(pk)
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)

#     # ✅ Handle PUT request to update category
#     def put(self, request, pk):
#         category = self.get_object(pk)
#         serializer = CategorySerializer(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     # ✅ Handle DELETE request to remove category
#     def delete(self, request, pk):
#         category = self.get_object(pk)
#         category.delete()
#         return Response({'message': 'Category deleted'}, status=204)


class CategoryListCreateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class CategoryDetailAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        print("Request data:", request.data)
        print("Request keys:", list(request.data.keys()))
        print("Raw subcategories:", request.data.get('subcategories'))

        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
        


    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response({'message': 'Category deleted'}, status=204)

class SevenCategoriesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.order_by('?')[:7]
        serializer = CategorySerializer(categories, many=True)
        return Response({
            "categories": serializer.data
        }, status=status.HTTP_200_OK)


# Metal API
class MetalListCreateAPIView(BaseListCreateAPIView):
    model = Metal
    serializer_class = MetalSerializer

class MetalDetailAPIView(BaseDetailAPIView):
    model = Metal
    serializer_class = MetalSerializer

# Stone API
class StoneListCreateAPIView(BaseListCreateAPIView):
    model = Gemstone
    serializer_class = StoneSerializer

class StoneDetailAPIView(BaseDetailAPIView):
    model = Gemstone
    serializer_class = StoneSerializer

# class NavbarCategoryListCreateAPIView(generics.ListCreateAPIView):
#     queryset = NavbarCategory.objects.all().order_by('order')
#     serializer_class = NavbarCategorySerializer

# class NavbarCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = NavbarCategory.objects.all()
#     serializer_class = NavbarCategorySerializer
#     lookup_field = 'pk'

class NavbarCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = NavbarCategory.objects.all().order_by('order')
    serializer_class = NavbarCategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        for index, item in enumerate(queryset, start=1):
            name = item.get_name()
            image = item.get_image()
            if name and image:
                data.append({
                    "index": index,
                    "name": name,
                    "image": image
                })
        return Response(data)

class NavbarCategoryMegaAPIView(ListAPIView):
    queryset = NavbarCategory.objects.all()
    serializer_class = NavbarCategoryMegaSerializer



class NavbarCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NavbarCategory.objects.all()
    serializer_class = NavbarCategorySerializer
class NavbarCategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NavbarCategory.objects.all()
    serializer_class = NavbarCategorySerializer

# Occasion API
class OccasionListCreateAPIView(BaseListCreateAPIView):
    model = Occasion
    serializer_class = OccasionSerializer

class OccasionDetailAPIView(BaseDetailAPIView):
    model = Occasion
    serializer_class = OccasionSerializer

# Gender API
class GenderListCreateAPIView(BaseListCreateAPIView):
    model = Gender
    serializer_class = GenderSerializer

class GenderDetailAPIView(BaseDetailAPIView):
    model = Gender
    serializer_class = GenderSerializer

class ContactListCreateAPIView(BaseListCreateAPIView):
    model = Contact
    serializer_class = ContactSerializer

class ContactDetailAPIView(BaseDetailAPIView):
    model = Contact
    serializer_class = ContactSerializer
    
class ProductFilterAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()

        # Retrieve query parameters from the request
        category = self.request.query_params.get('category')
        metal = self.request.query_params.get('metal')
        material = self.request.query_params.get('material')
        occasion = self.request.query_params.get('occasion')
        gender = self.request.query_params.get('gender')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        stone = self.request.query_params.get('stone')
        is_handcrafted = self.request.query_params.get('is_handcrafted')

        # Apply filters based on the query parameters
        if category:
            queryset = queryset.filter(category__name__iexact=category)
        if metal:
            queryset = queryset.filter(metal__name__iexact=metal)
        if material:
            queryset = queryset.filter(metal__material__name__iexact=material)
        if occasion:
            queryset = queryset.filter(occasions__name__iexact=occasion)
        if gender:
            queryset = queryset.filter(gender__name__iexact=gender)
        if price_min:
            queryset = queryset.filter(grand_total__gte=price_min)
        if price_max:
            queryset = queryset.filter(grand_total__lte=price_max)
        if stone:
            queryset = queryset.filter(productstone__stone__name__iexact=stone)
        if is_handcrafted is not None:
            if is_handcrafted.lower() == 'true':
                queryset = queryset.filter(is_handcrafted=True)
            elif is_handcrafted.lower() == 'false':
                queryset = queryset.filter(is_handcrafted=False)

       
        # Return distinct products based on the applied filters
        return queryset.distinct()
    


class ProductSearchAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        is_handcrafted = self.request.query_params.get('is_handcrafted', None)

        if query:
            queryset = Product.objects.filter(
                Q(head__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query) |
                Q(metal__name__icontains=query) |
                Q(metal__material__name__icontains=query) |
                Q(gender__name__icontains=query) |
                Q(occasion__name__icontains=query) |  # fixed field name here
                Q(stones__name__icontains=query)
            ).distinct()
        else:
            queryset = Product.objects.all()

        # Apply handcrafted filter if provided
        if is_handcrafted is not None:
            if is_handcrafted.lower() == 'true':
                queryset = queryset.filter(is_handcrafted=True)
            elif is_handcrafted.lower() == 'false':
                queryset = queryset.filter(is_handcrafted=False)

        return queryset
    
    
class ProductShareAPIView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product_url = request.build_absolute_uri(f'/api/products/{product.pk}/')

        product_image = None
        if isinstance(product.images, list) and product.images:
            product_image = product.images[0]

        # 🎉 Share message with brand + greeting
        share_text = (
            f"Hey! Check this out from *My Jewelry My Design* \n\n"
            f"{product.head}\n"
            f"Price: ₹{product.grand_total}\n"
            f"Rating: {product.average_rating}/5\n"
            f"Shop Now: {product_url}\n\n"
            f"Wishing you a sparkling day ahead!"
        )

        encoded_text = quote_plus(share_text)

        share_links = {
            "whatsapp": f"https://wa.me/?text={encoded_text}",
            "telegram": f"https://t.me/share/url?url={product_url}&text={quote_plus(product.head)}",
            "facebook": f"https://www.facebook.com/sharer/sharer.php?u={product_url}",
            "instagram": "https://www.instagram.com/"  # Placeholder only
        }

        return Response({
            "product_id": product.pk,
            "product_head": product.head,
            "product_url": product_url,
            "product_image": product_image,
            "grand_total": str(product.grand_total),
            "average_rating": product.average_rating,
            "share_links": share_links
        }, status=status.HTTP_200_OK)

class ProductPreviewView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product_image = product.images[0] if isinstance(product.images, list) and product.images else None

        return render(request, "product_preview.html", {
            "product": product,
            "product_image": product_image,
            "product_url": request.build_absolute_uri()
        })
class ProductStoneListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductStone.objects.all()
    serializer_class = ProductStoneSerializer


class ProductStoneDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductStone.objects.all()
    serializer_class = ProductStoneSerializer



class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # Check if the user exists
            try:
                user = Register.objects.get(username=username)
                # Manually check the password hash
                if check_password(password, user.password):  # Use check_password to validate hashed password
                    # Generate JWT tokens on successful authentication
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })
                else:
                    return Response({"detail": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)
            except Register.DoesNotExist:
                return Response({"detail": "Invalid username."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(f"New User Registered with ID: {user.id}")

            # Check if UserProfile already exists (prevent duplicates)
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(
                    username=user,  # OneToOneField to Register
                    full_name=user.username,
                    phone_number=user.mobile
                )
                print("✅ UserProfile created for", user.username)

            return Response({
                "message": "User registered successfully",
                "register": RegisterSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RegisterListView(APIView):
    def get(self, request, *args, **kwargs):
        users = Register.objects.all()
        serializer = RegisterSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterDetailView(APIView):
    def get(self, request, id, *args, **kwargs):
        user = get_object_or_404(Register, id=id)
        serializer = RegisterSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)



class UserProfileListView(APIView):
    def get(self, request, *args, **kwargs):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileCreateView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def perform_create(self, serializer):
        register_id = self.request.data.get('username')
        register_instance = get_object_or_404(Register, id=register_id)
        serializer.save(username=register_instance)


class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return get_object_or_404(UserProfile, id=self.kwargs["id"])


class UserProfileDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(username=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        if UserProfile.objects.filter(username=request.user).exists():
            return Response({"detail": "Profile already exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            # Ensure the user agreed to the privacy policy
            if not serializer.validated_data.get('agree'):
                return Response({"agree": ["You must agree to the privacy policy."]},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer.save(username=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            profile = UserProfile.objects.get(username=request.user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileImageUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            profile = UserProfile.objects.get(username=request.user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileImageSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            image_path = serializer.data['image']

            # ✅ Construct full Cloudinary URL
            cloud_name = getattr(settings, 'CLOUDINARY_STORAGE', {}).get('CLOUD_NAME', 'your-default-cloud-name')
            full_url = f"https://res.cloudinary.com/{cloud_name}/{image_path}"

            return Response({
                "message": "Profile image updated successfully",
                "image_url": full_url
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutAPIView(APIView):
    def post(self, request):
        # Call Django's built-in logout function to clear the session
        logout(request)
        
        # Return a success response
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
   
User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
from rest_framework.permissions import IsAdminUser
import os
from rest_framework import parsers
from .utils import send_whatsapp_message
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
ADMIN_WHATSAPP_NUMBER = os.getenv("ADMIN_WHATSAPP_NUMBER")

if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, ADMIN_WHATSAPP_NUMBER]):
    raise ImproperlyConfigured("One or more Twilio environment variables are missing.")

class ProductEnquiryAPIView(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        data = request.data.copy()
        data['product'] = str(product.id)

        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                data.setdefault('name', profile.full_name)
                data.setdefault('email', profile.email)
                data.setdefault('phone', profile.phone_number)
            except Exception:
                pass

        serializer = ProductEnquirySerializer(data=data)
        if serializer.is_valid():
            enquiry = serializer.save()
            try:
                self.send_whatsapp_message(enquiry)
            except Exception as e:
                print("WhatsApp error:", e)

            return Response({"message": "Enquiry submitted successfully."}, status=201)

        return Response(serializer.errors, status=400)

    def send_whatsapp_message(self, enquiry):
        image_url = enquiry.product.images[0] if enquiry.product.images else "No image available"
        message_text = enquiry.get_message_or_default()

        message = f"""
🟡 *New Product Enquiry!*

📦 Product ID: {enquiry.product.id}
📦 Product: {enquiry.product.head}
📦 Quantity: {enquiry.quantity}

👤 Name: {enquiry.name}
📧 Email: {enquiry.email}
📱 Phone: {enquiry.phone}

💬 Message: {message_text}

🗌 Image: {image_url}
"""
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            to=ADMIN_WHATSAPP_NUMBER,
            body=message.strip()
        )



class ProductEnquiryListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        enquiries = ProductEnquiry.objects.all().order_by('-created_at')
        serializer = ProductEnquirySerializer(enquiries, many=True)
        return Response(serializer.data)
    
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class WishlistAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        wishlist = Wishlist.objects.filter(user=user).select_related('product')
        serializer = WishlistSerializer(wishlist, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "product_id is required"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)

        _, created = Wishlist.objects.get_or_create(user=user, product=product)
        if created:
            return Response({"message": "Product added to wishlist"}, status=201)
        return Response({"message": "Product already in wishlist"}, status=200)


class WishlistDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, product_id):
        user = request.user
        try:
            wishlist_item = Wishlist.objects.get(user=user, product_id=product_id)
        except Wishlist.DoesNotExist:
            return Response({"error": "Product not in wishlist"}, status=404)

        wishlist_item.delete()
        return Response({"message": "Removed from wishlist"}, status=204)

    def get(self, request, product_id):
        user = request.user
        try:
            wishlist_item = Wishlist.objects.select_related('product').get(user=user, product_id=product_id)
        except Wishlist.DoesNotExist:
            return Response({"error": "Product not in wishlist"}, status=404)

        serializer = WishlistSerializer(wishlist_item, context={'request': request})
        return Response(serializer.data, status=200)




class UserLoginView(APIView):
    permission_classes = []  # No authentication required for login

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Please provide both username and password"}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate securely
        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"error": "User account is disabled"}, status=status.HTTP_403_FORBIDDEN)

        # Identify user type
        user_type = "customer"
        if user.is_superuser:
            user_type = "superuser"

        # Generate JWT tokens manually
        tokens = get_tokens_for_user(user)

        response_data = {
            "message": "Login successful",
            "access_token": tokens["access"],
            "refresh_token": tokens["refresh"],
            "username": user.username,
            "user_type": user_type,
        }

        return Response(response_data, status=status.HTTP_200_OK) 
    

class RecommendProductsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        username = request.query_params.get('username')

        # Step 1: Try to fetch user visits if username is provided
        if username:
            try:
                user = Register.objects.get(username=username)
                visits = UserVisit.objects.filter(user=user).order_by('-timestamp')[:5]
                visited_products = Product.objects.filter(id__in=visits.values_list('product_id', flat=True))

                if visited_products.exists():
                    serializer = ProductSerializer(
                        visited_products,
                        many=True,
                        context={'request': request}  # ✅ Important
                    )
                    return Response({
                        "type": "related",
                        "products": serializer.data
                    }, status=status.HTTP_200_OK)

            except Register.DoesNotExist:
                pass  # If user doesn't exist, proceed to fallback

        # Step 2: Fallback - pick a random category that has products
        categories_with_products = Category.objects.filter(product__isnull=False).distinct()

        if categories_with_products.exists():
            for category in categories_with_products.order_by('?'):
                products = Product.objects.filter(category=category)[:5]
                if products.exists():
                    serializer = ProductSerializer(
                        products,
                        many=True,
                        context={'request': request}  # ✅ Important
                    )
                    return Response({
                        "type": "random_category",
                        "category": category.name,
                        "products": serializer.data
                    }, status=status.HTTP_200_OK)

        # Step 3: Final fallback - get any products if nothing above works
        fallback_products = Product.objects.all()[:5]
        if fallback_products.exists():
            serializer = ProductSerializer(
                fallback_products,
                many=True,
                context={'request': request}  # ✅ Important
            )
            return Response({
                "type": "fallback_all",
                "products": serializer.data
            }, status=status.HTTP_200_OK)

        # Step 4: No products at all
        return Response({
            "message": "No products found"
        }, status=status.HTTP_404_NOT_FOUND)

    

class HeaderListCreateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        slider_images = request.FILES.getlist('slider_images')
        main_imgs = request.FILES.getlist('main_img')
        main_mobile_imgs = request.FILES.getlist('main_mobile_img')

        uploaded_slider_images = []
        uploaded_main_imgs = []
        uploaded_main_mobile_imgs = []

        for img in slider_images:
            uploaded_slider_images.append(upload(img)['url'])

        for img in main_imgs:
            uploaded_main_imgs.append(upload(img)['url'])

        for img in main_mobile_imgs:
            uploaded_main_mobile_imgs.append(upload(img)['url'])

        header = Header.objects.create(
            slider_images=uploaded_slider_images,
            main_img=uploaded_main_imgs,
            main_mobile_img=uploaded_main_mobile_imgs
        )
        serializer = HeaderSerializer(header)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        headers = Header.objects.all()
        serializer = HeaderSerializer(headers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HeaderDetailAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, pk, *args, **kwargs):
        try:
            header = Header.objects.get(pk=pk)
        except Header.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = HeaderSerializer(header)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        try:
            header = Header.objects.get(pk=pk)
        except Header.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        slider_images = request.FILES.getlist('slider_images')
        main_imgs = request.FILES.getlist('main_img')
        main_mobile_imgs = request.FILES.getlist('main_mobile_img')

        uploaded_slider_images = []
        uploaded_main_imgs = []
        uploaded_main_mobile_imgs = []

        for img in slider_images:
            uploaded_slider_images.append(upload(img)['url'])

        for img in main_imgs:
            uploaded_main_imgs.append(upload(img)['url'])

        for img in main_mobile_imgs:
            uploaded_main_mobile_imgs.append(upload(img)['url'])

        header.slider_images = uploaded_slider_images
        header.main_img = uploaded_main_imgs
        header.main_mobile_img = uploaded_main_mobile_imgs
        header.save()

        serializer = HeaderSerializer(header)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        try:
            header = Header.objects.get(pk=pk)
        except Header.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        header.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class RecentProductsWithFallbackAPIView(ListAPIView):
    serializer_class = RecentProductSerializer

    def get_queryset(self):
        limit = int(self.request.query_params.get('limit', 20))
        days = int(self.request.query_params.get('days', 15))
        cutoff_date = timezone.now() - timedelta(days=days)

        recent_qs = Product.objects.filter(created_at__gte=cutoff_date).order_by('-id')[:limit]
        if recent_qs.exists():
            self.from_fallback = False
            return recent_qs
        fallback_qs = Product.objects.all().order_by('-id')[:limit]
        self.from_fallback = True
        return fallback_qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(
            queryset,
            many=True,
            context={
                'request': request,
                'user_id': request.user.id  # ✅ Make sure to pass user_id here
            }
        )
        return Response({
            "from_fallback": self.from_fallback,
            "count": len(serializer.data),
            "products": serializer.data
        })

    

# class ProductListByGender(ListAPIView):
#     serializer_class = ProductSerializer

#     def get_queryset(self):
#         gender_id = self.request.query_params.get('gender')
#         if gender_id:
#             return Product.objects.filter(gender_id=gender_id)
#         return Product.objects.all()
class ProductListByGender(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.handle_filter(request)

    def post(self, request, *args, **kwargs):
        return self.handle_filter(request, use_post=True)

    def handle_filter(self, request, use_post=False):
        data = request.data if use_post else request.query_params
        gender_id = data.get('gender')

        products = Product.objects.all()
        if gender_id:
            products = products.filter(gender_id=gender_id)

        def parse_list(key):
            if hasattr(data, 'getlist'):
                return [v for v in data.getlist(key) if v]
            val = data.get(key)
            if isinstance(val, list):
                return val
            elif isinstance(val, str):
                return [v.strip() for v in val.split(',') if v.strip()]
            return []

        # Parse filters
        subcategories = parse_list('subcategory')
        materials = parse_list('materials')
        gemstones = parse_list('gemstones')
        colors = parse_list('colors')
        brand = data.get('brand', '').strip()
        price_raw = data.get('price')

        # Parse price
        price_min = price_max = None
        try:
            if isinstance(price_raw, str) and '-' in price_raw:
                price_min, price_max = map(float, price_raw.split('-'))
            elif isinstance(price_raw, dict):
                price_min = float(price_raw.get('min', 0))
                price_max = float(price_raw.get('max', 1000000))
            elif isinstance(price_raw, str) and price_raw.strip().startswith('{'):
                price_dict = json.loads(price_raw)
                price_min = float(price_dict.get("min", 0))
                price_max = float(price_dict.get("max", 1000000))
        except Exception:
            price_min = price_max = None

        # Apply filters
        if subcategories:
            products = products.filter(Subcategories__sub_name__in=subcategories)
        if brand:
            products = products.filter(head__icontains=brand)
        if materials:
            products = products.filter(metal__material__name__in=materials)
        if gemstones:
            products = products.filter(productstone__stone__name__in=gemstones).distinct()
        if colors:
            products = products.filter(metal__color__in=colors)

        # Final price filter
        filtered_products = []
        for product in products:
            try:
                gt = float(product.grand_total)
                if price_min is not None and gt < price_min:
                    continue
                if price_max is not None and gt > price_max:
                    continue
                filtered_products.append(product)
            except:
                continue

        serializer = ProductSerializer(filtered_products, many=True)

        # Build filter metadata
        gender = Gender.objects.filter(id=gender_id).first() if gender_id else None
        gender_name = gender.name if gender else "All"

        if filtered_products:
            prices = [float(p.grand_total) for p in filtered_products]
            price_range = {
                "min": min(prices),
                "max": max(prices)
            }
        else:
            price_range = {
                "min": 0,
                "max": 0
            }

        metal_colors = Metal.objects.values_list("color", flat=True).distinct()
        colors_with_codes = []
        for color in metal_colors:
            color_name = str(color).strip().lower()
            try:
                hex_code = name_to_hex(color_name)
            except ValueError:
                hex_code = "#CCCCCC"
            colors_with_codes.append({
                "color": color,
                "code": hex_code
            })

        # Subcategories related to gender
        subcategory_ids = Product.objects.filter(gender_id=gender_id).values_list("Subcategories__id", flat=True).distinct()
        subcategories_qs = Subcategories.objects.filter(id__in=subcategory_ids).values("id", "sub_name")

        filter_category_data = [{
            "category": {
                "id": gender.id if gender else None,
                "name": gender_name
            },
            "subcategories": list(subcategories_qs),
            "price_range": price_range,
            "brand": "my jewelry my design",
            "materials": list(Material.objects.all().values("id", "name")),
            "gemstones": list(Gemstone.objects.all().values("id", "name")),
            "colors": colors_with_codes
        }]

        message = None
        if any([subcategories, materials, gemstones, colors, brand, price_raw]):
            message = "Filters Applied" if filtered_products else "No Matching Filters"

        return Response({
            "gender": gender_name,
            "products": serializer.data,
            "filter_category": filter_category_data,
            "message": message
        })

# class ProductListByGender(ListAPIView):
#     serializer_class = ProductSerializer

#     def get(self, request, *args, **kwargs):
#         gender_id = request.query_params.get('gender')
#         category_ids = request.query_params.getlist('category')
#         material_names = request.query_params.getlist('material')
#         gemstone_names = request.query_params.getlist('gemstone')
#         color_names = request.query_params.getlist('color')
#         price_min = request.query_params.get('price_min')
#         price_max = request.query_params.get('price_max')

#         # Base queryset
#         queryset = Product.objects.all()

#         if gender_id:
#             queryset = queryset.filter(gender_id=gender_id)
#         if category_ids:
#             queryset = queryset.filter(category_id__in=category_ids)
#         if material_names:
#             queryset = queryset.filter(metal__material__name__in=material_names)
#         if gemstone_names:
#             queryset = queryset.filter(productstone__stone__name__in=gemstone_names).distinct()
#         if color_names:
#             queryset = queryset.filter(metal__color__in=color_names)
#         if price_min and price_max:
#             queryset = queryset.filter(frozen_unit_price__gte=price_min, frozen_unit_price__lte=price_max)

#         serializer = self.get_serializer(queryset, many=True)

#         # Filter options
#         categories = Category.objects.all().values('id', 'name')
#         materials = Material.objects.all().values('id', 'name')
#         gemstones = Gemstone.objects.all().values('id', 'name')
#         colors = Metal.objects.values_list('color', flat=True).distinct()

#         price_range = Product.objects.aggregate(
#             min_price=Min('frozen_unit_price'),
#             max_price=Max('frozen_unit_price')
#         )

#         return Response({
#             "filter_options": {
#                 "categories": list(categories),
#                 "materials": list(materials),
#                 "gemstones": list(gemstones),
#                 "colors": list(colors),
#                 "price_range": {
#                     "min": price_range['min_price'] or 0,
#                     "max": price_range['max_price'] or 0
#                 }
#             },
#             "total_products": queryset.count(),
#             "products": serializer.data
#         }, status=status.HTTP_200_OK)


# class SevenCategoriesAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         categories = Category.objects.order_by('?')[:7]  # 7 random categories
#         serializer = CategorySerializer(categories, many=True)
#         return Response({"categories": serializer.data}, status=status.HTTP_200_OK)
class SevenCategoriesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.order_by('?')[:7]  # 7 random categories
        serializer = CategorySerializer(categories, many=True)

        # Remove 'subcategories' from all serialized categories
        cleaned_data = []
        for item in serializer.data:
            item.pop('subcategories', None)  # remove if exists
            cleaned_data.append(item)

        return Response({"categories": cleaned_data}, status=status.HTTP_200_OK)

# class SevenCategoryDetailAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk, *args, **kwargs):
#         user = request.user

#         # Get the category object or 404
#         category = get_object_or_404(Category, pk=pk)

#         # Get all products in the given category
#         products = Product.objects.filter(category=category)

#         # Serialize products with context for user-specific fields
#         serializer = FinestProductSerializer(
#             products, many=True, context={'user': user}
#         )

#         # Return the category name as string and serialized products
#         return Response({
#             "category": category.name,
#             "products": serializer.data
#         }, status=status.HTTP_200_OK)


# important
# class SevenCategoryDetailAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk, *args, **kwargs):
#         return self.handle_request(request, pk)

#     def post(self, request, pk, *args, **kwargs):
#         return self.handle_request(request, pk, filter_data=True)

#     def handle_request(self, request, pk, filter_data=False):
#         user = request.user
#         category = get_object_or_404(Category, pk=pk)

#         # Clear filter flag
#         clear_filter = request.data.get('clear', False) if filter_data else False

#         # Get base products
#         products = Product.objects.filter(category=category)

#         # Skip filtering if clear is true
#         if filter_data and not clear_filter:
#             data = request.data

#             def parse_list(field):
#                 if hasattr(data, 'getlist'):
#                     return data.getlist(field)
#                 val = data.get(field)
#                 return val if isinstance(val, list) else [val] if val else []

#             subcategories = parse_list('subcategory')
#             materials = parse_list('material')
#             gemstones = parse_list('gemstone')
#             colors = parse_list('color')
#             brand = data.get('brand')
#             price_min = data.get('price_min')
#             price_max = data.get('price_max')

#             try:
#                 price_min = float(price_min) if price_min else None
#                 price_max = float(price_max) if price_max else None
#             except ValueError:
#                 price_min = price_max = None

#             if subcategories:
#                 products = products.filter(Subcategories__id__in=subcategories)
#             if brand:
#                 products = products.filter(head__icontains=brand)
#             if materials:
#                 products = products.filter(metal__material__name__in=materials)
#             if gemstones:
#                 products = products.filter(productstone__stone__name__in=gemstones).distinct()
#             if colors:
#                 products = products.filter(metal__color__in=colors)

#         # Apply grand_total filtering (skip if clear)
#         product_list = []
#         for product in products:
#             gt = float(product.grand_total)

#             if filter_data and not clear_filter:
#                 price_min = float(request.data.get('price_min', 0) or 0)
#                 price_max = float(request.data.get('price_max', 0) or 0)
#                 if price_min and gt < price_min:
#                     continue
#                 if price_max and gt > price_max:
#                     continue

#             product_list.append({
#                 "id": product.id,
#                 "head": product.head,
#                 "description": product.description,
#                 "first_image": product.images[0] if product.images else None,
#                 "average_rating": product.average_rating,
#                 "grand_total": str(product.grand_total),
#                 "is_wishlisted": True  # Customize as needed
#             })

#         if product_list:
#             product_list.append({"message": "Products found"})
#         else:
#             product_list = [{"message": "No products found"}]

#         return Response({
#             "category": category.name,
#             "products": product_list
#         }, status=200)

from webcolors import name_to_hex



# class SevenCategoryDetailAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk, *args, **kwargs):
#         return self.handle_request(request, pk)

#     def post(self, request, pk, *args, **kwargs):
#         return self.handle_request(request, pk, filter_data=True)

#     def handle_request(self, request, pk, filter_data=False):
#         category = get_object_or_404(Category, pk=pk)
#         clear_filter = request.data.get('clear', False) if filter_data else False
#         products = Product.objects.filter(category=category)

#         price_min = price_max = None

#         if filter_data and not clear_filter:
#             data = request.data

#             def parse_list(field):
#                 if hasattr(data, 'getlist'):
#                     return data.getlist(field)
#                 val = data.get(field)
#                 return val if isinstance(val, list) else [val] if val else []

#             subcategories = parse_list('subcategory')
#             materials = parse_list('materials')
#             gemstones = parse_list('gemstones')
#             colors = parse_list('colors')
#             brand = data.get('brand')
#             price_raw = data.get('price')

#             print("📥 Subcategories (names):", subcategories)
#             print("📥 Materials (names):", materials)

#             if price_raw and "-" in price_raw:
#                 try:
#                     price_min, price_max = map(float, price_raw.split("-"))
#                 except ValueError:
#                     price_min = price_max = None

#             if subcategories:
#                 products = products.filter(Subcategories__sub_name__in=subcategories)
#             if brand:
#                 products = products.filter(head__icontains=brand)
#             if materials:
#                 products = products.filter(metal__material__name__in=materials)
#             if gemstones:
#                 products = products.filter(productstone__stone__name__in=gemstones).distinct()
#             if colors:
#                 products = products.filter(metal__color__in=colors)

#         # Build product list
#         product_list = []
#         for product in products:
#             gt = float(product.grand_total)
#             if filter_data and not clear_filter and price_min is not None and price_max is not None:
#                 if gt < price_min or gt > price_max:
#                     continue

#             print("✅ Matched Product:", product.head)

#             product_list.append({
#                 "id": product.id,
#                 "head": product.head,
#                 "description": product.description,
#                 "first_image": product.images[0] if product.images else None,
#                 "average_rating": product.average_rating,
#                 "grand_total": str(product.grand_total),
#                 "is_wishlisted": True  # Replace with actual logic if needed
#             })

#         # Set message
#         if filter_data and not clear_filter:
#             message = "Filters Applied" if product_list else "No Matching Filters"
#         else:
#             message = None

#         # Filter metadata
#         default_min = 0
#         default_max = 1000000

#         if filter_data:
#             try:
#                 price_min_val = float(request.data.get("price_min", default_min))
#                 price_max_val = float(request.data.get("price_max", default_max))
#             except ValueError:
#                 price_min_val = default_min
#                 price_max_val = default_max
#         else:
#             price_min_val = default_min
#             price_max_val = default_max

#         metal_colors = Metal.objects.values_list('color', flat=True).distinct()
#         colors_with_codes = []
#         for color in metal_colors:
#             color_name = str(color).strip().lower()
#             try:
#                 hex_code = name_to_hex(color_name)
#             except ValueError:
#                 hex_code = "#CCCCCC"
#             colors_with_codes.append({
#                 "color": color,
#                 "code": hex_code
#             })

#         filter_category_data = [{
#             "category": {
#                 "id": category.id,
#                 "name": category.name
#             },
#             "subcategories": list(Subcategories.objects.filter(category=category).values('id', 'sub_name')),
#             "price_range": {
#                 "min": price_min_val,
#                 "max": price_max_val
#             },
#             "brand": "my jewelry my design",
#             "materials": list(Material.objects.all().values('id', 'name')),
#             "gemstones": list(Gemstone.objects.all().values('id', 'name')),
#             "colors": colors_with_codes
#         }]

#         # Final response
#         response_data = {
#             "category": category.name,
#             "products": product_list,
#             "filter_category": filter_category_data
#         }

#         if message:
#             response_data["message"] = message

#         return Response(response_data, status=200)

# class SevenCategoryDetailAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk, *args, **kwargs):
#         return self.handle_request(request, pk)

#     def post(self, request, pk, *args, **kwargs):
#         return self.handle_request(request, pk, filter_data=True)

#     def handle_request(self, request, pk, filter_data=False):
#         category = get_object_or_404(Category, pk=pk)
#         clear_filter = request.data.get('clear', False) if filter_data else False
#         products = Product.objects.filter(category=category)

#         price_min = price_max = None

#         if filter_data and not clear_filter:
#             data = request.data

#             def parse_list(field):
#                 if hasattr(data, 'getlist'):
#                     return [v for v in data.getlist(field) if v]
#                 val = data.get(field)
#                 return [val] if val else []

#             # Parse inputs
#             subcategories = parse_list('subcategory')
#             materials = parse_list('materials')
#             gemstones = parse_list('gemstones')
#             colors = parse_list('colors')
#             brand = data.get('brand')
#             price_raw = data.get('price')

#             print("📥 Filters Received:")
#             print("Subcategories:", subcategories)
#             print("Materials:", materials)
#             print("Gemstones:", gemstones)
#             print("Colors:", colors)
#             print("Brand:", brand)
#             print("Price:", price_raw)

#             # Parse price range
#             if price_raw and "-" in price_raw:
#                 try:
#                     price_min, price_max = map(float, price_raw.split("-"))
#                 except ValueError:
#                     price_min = price_max = None

#             # Apply filters conditionally
#             if subcategories:
#                 products = products.filter(Subcategories__sub_name__in=subcategories)
#             if brand:
#                 products = products.filter(head__icontains=brand)
#             if materials:
#                 products = products.filter(metal__material__name__in=materials)
#             if gemstones:
#                 products = products.filter(productstone__stone__name__in=gemstones).distinct()
#             if colors:
#                 products = products.filter(metal__color__in=colors)

#         # Build product list
#         product_list = []
#         for product in products:
#             gt = float(product.grand_total)
#             if filter_data and not clear_filter and price_min is not None and price_max is not None:
#                 if gt < price_min or gt > price_max:
#                     continue

#             print("✅ Matched Product:", product.head)

#             product_list.append({
#                 "id": product.id,
#                 "head": product.head,
#                 "description": product.description,
#                 "first_image": product.images[0] if product.images else None,
#                 "average_rating": product.average_rating,
#                 "grand_total": str(product.grand_total),
#                 "is_wishlisted": True  # Replace with real check if needed
#             })

#         # Message logic
#         if filter_data and not clear_filter:
#             message = "Filters Applied" if product_list else "No Matching Filters"
#         else:
#             message = None

#         # Metadata
#         default_min = 0
#         default_max = 1000000
#         if filter_data:
#             try:
#                 price_min_val = float(request.data.get("price_min", default_min))
#                 price_max_val = float(request.data.get("price_max", default_max))
#             except ValueError:
#                 price_min_val = default_min
#                 price_max_val = default_max
#         else:
#             price_min_val = default_min
#             price_max_val = default_max

#         # Color conversion
#         metal_colors = Metal.objects.values_list('color', flat=True).distinct()
#         colors_with_codes = []
#         for color in metal_colors:
#             color_name = str(color).strip().lower()
#             try:
#                 hex_code = name_to_hex(color_name)
#             except ValueError:
#                 hex_code = "#CCCCCC"
#             colors_with_codes.append({
#                 "color": color,
#                 "code": hex_code
#             })

#         # Filter category metadata
#         filter_category_data = [{
#             "category": {
#                 "id": category.id,
#                 "name": category.name
#             },
#             "subcategories": list(Subcategories.objects.filter(category=category).values('id', 'sub_name')),
#             "price_range": {
#                 "min": price_min_val,
#                 "max": price_max_val
#             },
#             "brand": "my jewelry my design",
#             "materials": list(Material.objects.all().values('id', 'name')),
#             "gemstones": list(Gemstone.objects.all().values('id', 'name')),
#             "colors": colors_with_codes
#         }]

#         # Final response
#         response_data = {
#             "category": category.name,
#             "products": product_list,
#             "filter_category": filter_category_data
#         }
#         if message:
#             response_data["message"] = message

#         return Response(response_data, status=200)

from django.db.models import Min, Max

# class SevenCategoryDetailAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk, *args, **kwargs):
#         return self.handle_request(request, pk)

#     def post(self, request, pk, *args, **kwargs):
#         return self.handle_request(request, pk, filter_data=True)

#     def handle_request(self, request, pk, filter_data=False):
#         category = get_object_or_404(Category, pk=pk)
#         clear_filter = request.data.get('clear', False) if filter_data else False
#         products = Product.objects.filter(category=category)

#         price_min = price_max = None

#         if filter_data and not clear_filter:
#             data = request.data

#             def parse_list(field):
#                 if hasattr(data, 'getlist'):
#                     return [v for v in data.getlist(field) if v]
#                 val = data.get(field)
#                 return [val] if val else []

#             # Parse inputs
#             subcategories = parse_list('subcategory')
#             materials = parse_list('materials')
#             gemstones = parse_list('gemstones')
#             colors = parse_list('colors')
#             brand = data.get('brand')
#             price_raw = data.get('price')

#             print("📥 Filters Received:")
#             print("Subcategories:", subcategories)
#             print("Materials:", materials)
#             print("Gemstones:", gemstones)
#             print("Colors:", colors)
#             print("Brand:", brand)
#             print("Price:", price_raw)

#             # Parse price range
#             if price_raw and "-" in price_raw:
#                 try:
#                     price_min, price_max = map(float, price_raw.split("-"))
#                 except ValueError:
#                     price_min = price_max = None

#             # Apply filters
#             if subcategories:
#                 products = products.filter(Subcategories__sub_name__in=subcategories)
#             if brand:
#                 products = products.filter(head__icontains=brand)
#             if materials:
#                 products = products.filter(metal__material__name__in=materials)
#             if gemstones:
#                 products = products.filter(productstone__stone__name__in=gemstones).distinct()
#             if colors:
#                 products = products.filter(metal__color__in=colors)

#         # Build product list
#         product_list = []
#         for product in products:
#             gt = float(product.grand_total)
#             if filter_data and not clear_filter and price_min is not None and price_max is not None:
#                 if gt < price_min or gt > price_max:
#                     continue

#             print("✅ Matched Product:", product.head)

#             product_list.append({
#                 "id": product.id,
#                 "head": product.head,
#                 "description": product.description,
#                 "first_image": product.images[0] if product.images else None,
#                 "average_rating": product.average_rating,
#                 "grand_total": str(product.grand_total),
#                 "is_wishlisted": True  # Replace with actual logic
#             })

#         # Dynamic price range from filtered products
#         if product_list:
#             all_prices = [float(p['grand_total']) for p in product_list]
#             price_range = {
#                 "min": min(all_prices),
#                 "max": max(all_prices)
#             }
#         else:
#             price_range = {
#                 "min": 0,
#                 "max": 0
#             }

#         # Message logic
#         if filter_data and not clear_filter:
#             message = "Filters Applied" if product_list else "No Matching Filters"
#         else:
#             message = None

#         # Color conversion
#         metal_colors = Metal.objects.values_list('color', flat=True).distinct()
#         colors_with_codes = []
#         for color in metal_colors:
#             color_name = str(color).strip().lower()
#             try:
#                 hex_code = name_to_hex(color_name)
#             except ValueError:
#                 hex_code = "#CCCCCC"
#             colors_with_codes.append({
#                 "color": color,
#                 "code": hex_code
#             })

#         # Filter metadata block
#         filter_category_data = [{
#             "category": {
#                 "id": category.id,
#                 "name": category.name
#             },
#             "subcategories": list(Subcategories.objects.filter(category=category).values('id', 'sub_name')),
#             "price_range": price_range,
#             "brand": "my jewelry my design",
#             "materials": list(Material.objects.all().values('id', 'name')),
#             "gemstones": list(Gemstone.objects.all().values('id', 'name')),
#             "colors": colors_with_codes
#         }]

#         # Final response
#         response_data = {
#             "category": category.name,
#             "products": product_list,
#             "filter_category": filter_category_data
#         }
#         if message:
#             response_data["message"] = message

#         return Response(response_data, status=200)



class SevenCategoryDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        return self.handle_request(request, pk)

    def post(self, request, pk, *args, **kwargs):
        return self.handle_request(request, pk, filter_data=True)

    def handle_request(self, request, pk, filter_data=False):
        category = get_object_or_404(Category, pk=pk)
        clear_filter = request.data.get('clear', False) if filter_data else False
        products = Product.objects.filter(category=category)

        price_min = price_max = None

        if filter_data and not clear_filter:
            data = request.data

            def parse_list(field):
                if hasattr(data, 'getlist'):
                    return [v for v in data.getlist(field) if v]
                val = data.get(field)
                return [val] if val else []

            # Parse filters
            subcategories = parse_list('subcategory')
            materials = parse_list('materials')
            gemstones = parse_list('gemstones')
            colors = parse_list('colors')
            brand = data.get('brand')
            price_raw = data.get('price')

            print("📥 Filters Received:")
            print("Subcategories:", subcategories)
            print("Materials:", materials)
            print("Gemstones:", gemstones)
            print("Colors:", colors)
            print("Brand:", brand)
            print("Price:", price_raw)

            # Parse price filter (object or string)
            try:
                if isinstance(price_raw, str) and "-" in price_raw:
                    price_min, price_max = map(float, price_raw.split("-"))
                elif isinstance(price_raw, dict):
                    price_min = float(price_raw.get("min", 0))
                    price_max = float(price_raw.get("max", 1000000))
                elif isinstance(price_raw, str) and price_raw.strip().startswith("{"):
                    import json
                    price_dict = json.loads(price_raw)
                    price_min = float(price_dict.get("min", 0))
                    price_max = float(price_dict.get("max", 1000000))
            except (ValueError, TypeError, json.JSONDecodeError):
                price_min = price_max = None

            # Apply filters
            if subcategories:
                products = products.filter(Subcategories__sub_name__in=subcategories)
            if brand:
                products = products.filter(head__icontains=brand)
            if materials:
                products = products.filter(metal__material__name__in=materials)
            if gemstones:
                products = products.filter(productstone__stone__name__in=gemstones).distinct()
            if colors:
                products = products.filter(metal__color__in=colors)

        # Build filtered product list
        product_list = []
        for product in products:
            gt = float(product.grand_total)
            if filter_data and not clear_filter and price_min is not None and price_max is not None:
                if gt < price_min or gt > price_max:
                    continue

            print("✅ Matched Product:", product.head)

            product_list.append({
                "id": product.id,
                "head": product.head,
                "description": product.description,
                "first_image": product.images[0] if product.images else None,
                "average_rating": product.average_rating,
                "grand_total": str(product.grand_total),
                "is_wishlisted": True  # Replace with real logic if needed
            })

        # Build price_range from matched products
        if product_list:
            all_prices = [float(p["grand_total"]) for p in product_list]
            price_range = {
                "min": min(all_prices),
                "max": max(all_prices)
            }
        else:
            price_range = {
                "min": 0,
                "max": 0
            }

        # Filter metadata
        metal_colors = Metal.objects.values_list("color", flat=True).distinct()
        colors_with_codes = []
        for color in metal_colors:
            color_name = str(color).strip().lower()
            try:
                hex_code = name_to_hex(color_name)
            except ValueError:
                hex_code = "#CCCCCC"
            colors_with_codes.append({
                "color": color,
                "code": hex_code
            })

        filter_category_data = [{
            "category": {
                "id": category.id,
                "name": category.name
            },
            "subcategories": list(Subcategories.objects.filter(category=category).values("id", "sub_name")),
            "price_range": price_range,
            "brand": "my jewelry my design",
            "materials": list(Material.objects.all().values("id", "name")),
            "gemstones": list(Gemstone.objects.all().values("id", "name")),
            "colors": colors_with_codes
        }]

        message = None
        if filter_data and not clear_filter:
            message = "Filters Applied" if product_list else "No Matching Filters"

        # Final response
        response_data = {
            "category": category.name,
            "products": product_list,
            "filter_category": filter_category_data
        }
        if message:
            response_data["message"] = message

        return Response(response_data, status=200)




def get_filtered_products(data, category):
    products = Product.objects.filter(category=category)

    def parse_list(field):
        if hasattr(data, 'getlist'):
            return data.getlist(field)
        val = data.get(field)
        return val if isinstance(val, list) else [val] if val else []

    subcategories = parse_list('subcategory')
    materials = parse_list('material')
    gemstones = parse_list('gemstone')
    colors = parse_list('color')
    brand = data.get('brand')
    price_min = data.get('price_min')
    price_max = data.get('price_max')

    try:
        price_min = float(price_min) if price_min else None
        price_max = float(price_max) if price_max else None
    except ValueError:
        price_min = price_max = None

    if subcategories:
        products = products.filter(Subcategories__id__in=subcategories)
    if brand:
        products = products.filter(head__icontains=brand)
    if materials:
        products = products.filter(metal__material__name__in=materials)
    if gemstones:
        products = products.filter(productstone__stone__name__in=gemstones).distinct()
    if colors:
        products = products.filter(metal__color__in=colors)

    filtered = []
    for product in products:
        gt = float(product.grand_total)
        if price_min and gt < price_min:
            continue
        if price_max and gt > price_max:
            continue
        filtered.append(product)

    return filtered

# import webcolors
# from webcolors import name_to_hex
# class CategoryFilterOptionsAPIView(APIView):
#     def get(self, request, category_id, *args, **kwargs):
#         return self.build_filter_response(category_id)

#     def post(self, request, category_id, *args, **kwargs):
#         return self.build_filter_response(category_id, request.data)

#     def build_filter_response(self, category_id, data=None):
#         category = get_object_or_404(Category, pk=category_id)
#         default_min = 0
#         default_max = 1000000

#         if data:
#             try:
#                 price_min = float(data.get("price_min", default_min))
#                 price_max = float(data.get("price_max", default_max))
#             except ValueError:
#                 price_min = default_min
#                 price_max = default_max
#         else:
#             price_min = default_min
#             price_max = default_max

#         # Get distinct metal colors and convert to hex if known
#         metal_colors = Metal.objects.values_list('color', flat=True).distinct()
#         colors_with_codes = []

#         for color in metal_colors:
#             color_name = color.strip().lower()
#             try:
#                 hex_code = name_to_hex(color_name)
#             except ValueError:
#                 hex_code = "#CCCCCC"  # fallback if color name is not standard
#             colors_with_codes.append({
#                 "color": color,
#                 "code": hex_code
#             })

#         filter_category = {
#             "category": {
#                 "id": category.id,
#                 "name": category.name
#             },
#             "subcategories": list(
#                 Subcategories.objects.filter(category=category).values('id', 'sub_name')
#             ),
#             "price_range": {
#                 "min": price_min,
#                 "max": price_max
#             },
#             "brand": "my jewelry my design",
#             "materials": list(Material.objects.all().values('id', 'name')),
#             "gemstones": list(Gemstone.objects.all().values('id', 'name')),
#             "colors": colors_with_codes
#         }

#         return Response({"filter_category": filter_category}, status=status.HTTP_200_OK)

# class SevenCategoryDetailAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk, *args, **kwargs):
#         user = request.user
#         category = get_object_or_404(Category, pk=pk)
#         products = Product.objects.filter(category=category)
#         serializer = FinestProductSerializer(products, many=True, context={"user": user})
#         return Response({"category": category.name, "products": serializer.data}, status=status.HTTP_200_OK)

#     def post(self, request, pk, *args, **kwargs):
#         user = request.user
#         category = get_object_or_404(Category, pk=pk)
#         products = get_filtered_products(request.data, category)
#         serializer = FinestProductSerializer(products, many=True, context={"user": user})
#         return Response({"category": category.name, "products": serializer.data}, status=status.HTTP_200_OK)





# class CategoryFilterOptionsAPIView(APIView):
#     def get(self, request, category_id, *args, **kwargs):
#         category = get_object_or_404(Category, pk=category_id)

#         subcategories = request.query_params.getlist('subcategory')
#         price_min = request.query_params.get('price_min')
#         price_max = request.query_params.get('price_max')
#         brand = request.query_params.get('brand')
#         materials = request.query_params.getlist('material')
#         gemstones = request.query_params.getlist('gemstone')
#         colors = request.query_params.getlist('color')

#         try:
#             price_min = float(price_min) if price_min else None
#             price_max = float(price_max) if price_max else None
#         except ValueError:
#             price_min = price_max = None

#         # Initial queryset
#         products = Product.objects.filter(category=category)

#         if subcategories:
#             products = products.filter(Subcategories__id__in=subcategories)
#         if brand:
#             products = products.filter(head__icontains=brand)
#         if materials:
#             products = products.filter(metal__material__name__in=materials)
#         if gemstones:
#             products = products.filter(productstone__stone__name__in=gemstones).distinct()
#         if colors:
#             products = products.filter(metal__color__in=colors)

#         # Filter by grand_total in Python
#         filtered_products = []
#         all_grand_totals = []

#         for product in products:
#             gt = product.grand_total
#             all_grand_totals.append(gt)

#             if price_min and gt < price_min:
#                 continue
#             if price_max and gt > price_max:
#                 continue

#             filtered_products.append({
#                 "id": product.id,
#                 "head": product.head,
#                 "description": product.description,
#                 "first_image": product.images[0] if product.images else None,
#                 "average_rating": product.average_rating,
#                 "grand_total": str(gt),
#                 "is_wishlisted": False  # You can customize this logic
#             })

#         # Grand total range
#         if all_grand_totals:
#             min_gt = min(all_grand_totals)
#             max_gt = max(all_grand_totals)
#         else:
#             min_gt = max_gt = 0

#         return Response({
#             "filter_category": {
#                 "category": {
#                     "id": category.id,
#                     "name": category.name
#                 },
#                 "subcategories": list(Subcategories.objects.filter(category=category).values('id', 'sub_name')),
#                 "price_range": {
#                     "min": float(min_gt),
#                     "max": float(max_gt)
#                 },
#                 "brand": "my jewelry my design",
#                 "materials": list(Material.objects.all().values('id', 'name')),
#                 "gemstones": list(Gemstone.objects.all().values('id', 'name')),
#                 "colors": list(Metal.objects.values_list('color', flat=True).distinct())
#             },
#             "total_products": len(filtered_products),
#             "products": filtered_products
#         }, status=status.HTTP_200_OK)


# class CategoryFilterOptionsAPIView(APIView):
#     def get_data(self, request):
#         # Support both GET and POST
#         return request.query_params if request.method == 'GET' else request.data

#     def get(self, request, category_id, *args, **kwargs):
#         return self.process(request, category_id)

#     def post(self, request, category_id, *args, **kwargs):
#         return self.process(request, category_id)

#     def process(self, request, category_id):
#         category = get_object_or_404(Category, pk=category_id)
#         data = self.get_data(request)

#         # Optional filters
#         subcategories = data.getlist('subcategory')
#         price_min = data.get('price_min')
#         price_max = data.get('price_max')
#         brand = data.get('brand')
#         materials = data.getlist('material')
#         gemstones = data.getlist('gemstone')
#         colors = data.getlist('color')

#         # Parse price range
#         try:
#             price_min = float(price_min) if price_min else None
#             price_max = float(price_max) if price_max else None
#         except ValueError:
#             price_min = price_max = None

#         # Initial DB query
#         products = Product.objects.filter(category=category)

#         if subcategories:
#             products = products.filter(Subcategories__id__in=subcategories)
#         if brand:
#             products = products.filter(head__icontains=brand)
#         if materials:
#             products = products.filter(metal__material__name__in=materials)
#         if gemstones:
#             products = products.filter(productstone__stone__name__in=gemstones).distinct()
#         if colors:
#             products = products.filter(metal__color__in=colors)

#         # Python-level grand_total filtering
#         filtered_products = []
#         all_grand_totals = []

#         for product in products:
#             gt = product.grand_total
#             all_grand_totals.append(gt)

#             if price_min is not None and gt < price_min:
#                 continue
#             if price_max is not None and gt > price_max:
#                 continue

#             filtered_products.append({
#                 "id": product.id,
#                 "head": product.head,
#                 "description": product.description,
#                 "first_image": product.images[0] if product.images else None,
#                 "average_rating": product.average_rating,
#                 "grand_total": str(gt),
#                 "is_wishlisted": False  # customize if needed
#             })

#         # Grand total range for UI
#         min_gt = float(min(all_grand_totals)) if all_grand_totals else 0
#         max_gt = float(max(all_grand_totals)) if all_grand_totals else 0

#         return Response({
#             "filter_category": {
#                 "category": {
#                     "id": category.id,
#                     "name": category.name
#                 },
#                 "subcategories": list(Subcategories.objects.filter(category=category).values('id', 'sub_name')),
#                 "price_range": {
#                     "min": min_gt,
#                     "max": max_gt
#                 },
#                 "brand": "my jewelry my design",
#                 "materials": list(Material.objects.all().values('id', 'name')),
#                 "gemstones": list(Gemstone.objects.all().values('id', 'name')),
#                 "colors": list(Metal.objects.values_list('color', flat=True).distinct())
#             },
#             "total_products": len(filtered_products),
#             "products": filtered_products,
#             "message": "products fetched successfully" if filtered_products else "no product available"
#         }, status=status.HTTP_200_OK)

# class CategoryFilterOptionsAPIView(APIView):
#     def post(self, request, category_id, *args, **kwargs):
#         from django.db.models import Q
#         category = get_object_or_404(Category, pk=category_id)

#         data = request.data

#         def parse_list(value):
#             if hasattr(data, 'getlist'):
#                 return data.getlist(value)
#             return data.get(value, []) if isinstance(data.get(value), list) else [data.get(value)] if data.get(value) else []

#         subcategories = parse_list('subcategory')
#         materials = parse_list('material')
#         gemstones = parse_list('gemstone')
#         colors = parse_list('color')
#         brand = data.get('brand')
#         price_min = data.get('price_min')
#         price_max = data.get('price_max')

#         try:
#             price_min = float(price_min) if price_min else None
#             price_max = float(price_max) if price_max else None
#         except ValueError:
#             price_min = price_max = None

#         # Base Query
#         products = Product.objects.filter(category=category)

#         # Safe filters
#         if subcategories:
#             valid_sub_ids = Subcategories.objects.filter(id__in=subcategories).values_list('id', flat=True)
#             if valid_sub_ids:
#                 products = products.filter(Subcategories__id__in=valid_sub_ids)
#             else:
#                 products = Product.objects.none()

#         if brand:
#             products = products.filter(head__icontains=brand)

#         if materials:
#             valid_mat = Material.objects.filter(name__in=materials).values_list('name', flat=True)
#             if valid_mat:
#                 products = products.filter(metal__material__name__in=valid_mat)
#             else:
#                 products = Product.objects.none()

#         if gemstones:
#             valid_gems = Gemstone.objects.filter(name__in=gemstones).values_list('name', flat=True)
#             if valid_gems:
#                 products = products.filter(productstone__stone__name__in=valid_gems).distinct()
#             else:
#                 products = Product.objects.none()

#         if colors:
#             valid_colors = Metal.objects.filter(color__in=colors).values_list('color', flat=True)
#             if valid_colors:
#                 products = products.filter(metal__color__in=valid_colors)
#             else:
#                 products = Product.objects.none()

#         # Final product filtering by grand_total
#         filtered_products = []
#         grand_totals = []

#         for product in products:
#             gt = float(product.grand_total)
#             grand_totals.append(gt)
#             if price_min is not None and gt < price_min:
#                 continue
#             if price_max is not None and gt > price_max:
#                 continue
#             filtered_products.append({
#                 "id": product.id,
#                 "head": product.head,
#                 "description": product.description,
#                 "first_image": product.images[0] if product.images else None,
#                 "average_rating": product.average_rating,
#                 "grand_total": str(product.grand_total),
#                 "is_wishlisted": False
#             })

#         price_range = {
#             "min": float(min(grand_totals)) if grand_totals else 0,
#             "max": float(max(grand_totals)) if grand_totals else 0
#         }

#         return Response({
#             "filter_category": {
#                 "category": {
#                     "id": category.id,
#                     "name": category.name
#                 },
#                 "subcategories": list(Subcategories.objects.filter(category=category).values('id', 'sub_name')),
#                 "price_range": price_range,
#                 "brand": "my jewelry my design",
#                 "materials": list(Material.objects.all().values('id', 'name')),
#                 "gemstones": list(Gemstone.objects.all().values('id', 'name')),
#                 "colors": list(Metal.objects.values_list('color', flat=True).distinct())
#             },
#             "total_products": len(filtered_products),
#             "products": filtered_products,
#             "message": "products fetched successfully" if filtered_products else "no product available"
#         }, status=status.HTTP_200_OK)


# important
# class CategoryFilterOptionsAPIView(APIView):
#     def post(self, request, category_id, *args, **kwargs):
#         from django.db.models import Min, Max

#         category = get_object_or_404(Category, pk=category_id)

#         # All products under the category
#         products = Product.objects.filter(category=category)

#         # Get grand total values for min and max
#         grand_totals = [float(p.grand_total) for p in products]
#         price_range = {
#             "min": min(grand_totals) if grand_totals else 0,
#             "max": max(grand_totals) if grand_totals else 0
#         }

#         # Build response
#         filter_category = {
#             "category": {
#                 "id": category.id,
#                 "name": category.name
#             },
#             "subcategories": list(
#                 Subcategories.objects.filter(category=category).values('id', 'sub_name')
#             ),
#             "price_range": price_range,
#             "brand": "my jewelry my design",  # Static or customize as needed
#             "materials": list(Material.objects.all().values('id', 'name')),
#             "gemstones": list(Gemstone.objects.all().values('id', 'name')),
#             "colors": list(Metal.objects.values_list('color', flat=True).distinct())
#         }

#         return Response({
#             "filter_category": filter_category
#         }, status=status.HTTP_200_OK)

# class CategoryFilterOptionsAPIView(APIView):
#     def get(self, request, category_id, *args, **kwargs):
#         return self.build_filter_response(category_id)

#     def post(self, request, category_id, *args, **kwargs):
#         return self.build_filter_response(category_id)

#     def build_filter_response(self, category_id):
#         category = get_object_or_404(Category, pk=category_id)
#         products = Product.objects.filter(category=category)

#         grand_totals = [float(p.grand_total) for p in products]
#         price_range = {
#             "min": min(grand_totals) if grand_totals else 0,
#             "max": max(grand_totals) if grand_totals else 0
#         }

#         filter_category = {
#             "category": {
#                 "id": category.id,
#                 "name": category.name
#             },
#             "subcategories": list(
#                 Subcategories.objects.filter(category=category).values('id', 'sub_name')
#             ),
#             "price_range": price_range,
#             "brand": "my jewelry my design",
#             "materials": list(Material.objects.all().values('id', 'name')),
#             "gemstones": list(Gemstone.objects.all().values('id', 'name')),
#             "colors": list(Metal.objects.values_list('color', flat=True).distinct())
#         }

#         return Response({
#             "filter_category": [filter_category]  # 👈 wrapped in a list
#         }, status=status.HTTP_200_OK)


class RelatedProductsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        product_id = request.query_params.get('product_id')

        if not product_id:
            return Response({"error": "product_id query param is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get related products in the same category but exclude the current product
        related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:10]

        # ✅ Pass context for is_wishlisted to work
        serializer = ProductSerializer(related_products, many=True, context={'request': request})
        return Response({"related_products": serializer.data}, status=status.HTTP_200_OK)
    
class ProductRatingAPIView(APIView):

    def post(self, request):
        serializer = ProductRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            rating = get_object_or_404(ProductRating, pk=pk)
            serializer = ProductRatingSerializer(rating)
            return Response(serializer.data)
        else:
            ratings = ProductRating.objects.all()
            serializer = ProductRatingSerializer(ratings, many=True)
            return Response(serializer.data)

    def put(self, request, pk):
        rating = get_object_or_404(ProductRating, pk=pk)
        serializer = ProductRatingSerializer(rating, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class NavbarCategorySubDataAPIView(APIView):
    def get(self, request):
        data = {
            "All Jewellery": {
                "categories": [
                    {"id": 1, "label": "All Jewellery", "icon": "/icons/jewel.svg"},
                    {"id": 2, "label": "Bangles", "icon": "/icons/jewel.svg"},
                    {"id": 3, "label": "Nose Pin", "icon": "/icons/jewel.svg"},
                    {"id": 4, "label": "Finger Rings", "icon": "/icons/jewel.svg"}
                ],
                "occasions": [
                    {"id": 1, "label": "Office wear", "icon": "/public/assets/Images/subcategory/occasions/o1.png"},
                    {"id": 2, "label": "Casual wear", "icon": "/public/assets/Images/subcategory/occasions/o2.png"},
                    {"id": 3, "label": "Modern wear", "icon": "/public/assets/Images/subcategory/occasions/o3.png"},
                    {"id": 4, "label": "Traditional wear", "icon": "/public/assets/Images/subcategory/occasions/o4.png"}
                ],
                "price": [
                    {"id": 1, "label": "<25K", "icon": "/public/assets/Images/subcategory/rate/r1.png"},
                    {"id": 2, "label": "25K - 50K", "icon": "/public/assets/Images/subcategory/rate/r2.png"},
                    {"id": 3, "label": "50K - 1L", "icon": "/public/assets/Images/subcategory/rate/r3.png"},
                    {"id": 4, "label": "1L & Above", "icon": "/public/assets/Images/subcategory/rate/r4.png"}
                ],
                "gender": [
                    {"id": 1, "label": "Women", "icon": "/public/assets/Images/subcategory/gender/f.png"},
                    {"id": 2, "label": "Men", "icon": "/public/assets/Images/subcategory/gender/m.png"},
                    {"id": 3, "label": "Kid", "icon": "/public/assets/Images/subcategory/gender/k.png"}
                ]
            }
        }
        return Response(data)
    

class NavbarCategorySubDataAPIView(APIView):
    def get(self, request):
        grouped_data = {}
        all_types = ['categories', 'occasions', 'price', 'gender']

        for category_type in all_types:
            subcategories = SubCategory.objects.filter(type=category_type)
            serialized = SubCategorySerializer(subcategories, many=True).data
            grouped_data[category_type] = serialized

        # You can change the key from "All Jewellery" to something dynamic too.
        return Response({"All Jewellery": grouped_data})
    


class MegaNavbar(APIView):
    def get(self, request):
        response_data = []

        # Static price ranges
        price_ranges = [
            { "id": 1, "label": "<25K", "icon": "/public/assets/Images/subcategory/rate/r1.png" },
            { "id": 2, "label": "25K - 50K", "icon": "/public/assets/Images/subcategory/rate/r2.png" },
            { "id": 3, "label": "50K - 1L", "icon": "/public/assets/Images/subcategory/rate/r3.png" },
            { "id": 4, "label": "1L & Above", "icon": "/public/assets/Images/subcategory/rate/r4.png" },
        ]

        #  Special "All Jewellery" option
        all_categories = Category.objects.all()
        all_occasions = Occasion.objects.all()
        all_genders = Gender.objects.all()

        all_jewellery_data = {
            "id": 0,
            "title": "All Jewellery",
            "image": "/icons/jewel.svg",
            "description": "Elegant handcrafted gold jewelry.",
            "mega": {
                "Category": [
                    {
                        "id": cat.id,
                        "label": cat.name,
                        "icon": cat.image.url
                    } for cat in all_categories
                ],
                "Occasions": [
                    {
                        "id": occ.id,
                        "label": occ.name,
                        "icon": occ.image.url
                    } for occ in all_occasions
                ],
                "Price": price_ranges,
                "Gender": [
                    {
                        "id": g.id,
                        "label": g.name,
                        "icon": g.image.url
                    } for g in all_genders
                ]
            }
        }
        response_data.append(all_jewellery_data)

        #  For each Material with linked Products
        materials = Material.objects.all()
        for material in materials:
            products = Product.objects.filter(metal__material=material)

            if not products.exists():
                continue  # Skip materials with no products

            # Extract related category/occasion/gender
            related_categories = Category.objects.filter(product__in=products).distinct()
            related_occasions = Occasion.objects.filter(product__in=products).distinct()
            related_genders = Gender.objects.filter(product__in=products).distinct()

            material_data = {
                "id": material.id,
                "title": material.name,
                "image": "/icons/jewel.svg",
                "description": f"{material.name} based elegant jewelry.",
                "mega": {
                    "Category": [
                        {
                            "id": cat.id,
                            "label": cat.name,
                            "icon": cat.image.url
                        } for cat in related_categories
                    ],
                    "Occasions": [
                        {
                            "id": occ.id,
                            "label": occ.name,
                            "icon": occ.image.url
                        } for occ in related_occasions
                    ],
                    "Price": price_ranges,
                    "Gender": [
                        {
                            "id": g.id,
                            "label": g.name,
                            "icon": g.image.url
                        } for g in related_genders
                    ]
                }
            }

            response_data.append(material_data)

        return Response(response_data, status=status.HTTP_200_OK)







class CombinedSuggestionsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user if request.user.is_authenticated else None
        query = request.GET.get('query', '').strip()

        suggested_categories = []
        suggested_products = []
        popular_categories = []
        popular_products = []

        if query:
            # Show suggestions based on query (material or category/product name)
            material_match = Material.objects.filter(name__icontains=query).first()
            if material_match:
                suggested_categories = Category.objects.filter(
                    product__metal__material=material_match
                ).distinct()
                if not suggested_categories.exists():
                    suggested_categories = Category.objects.filter(name__icontains=query)
            else:
                suggested_categories = Category.objects.filter(name__icontains=query)

            suggested_products = Product.objects.filter(head__icontains=query)

        else:
            # Show popular items when no query is provided
            pop_cat_ids = (
                UserVisit.objects
                .values('product__category')
                .annotate(visits=Count('id'))
                .order_by('-visits')
                .values_list('product__category', flat=True)[:5]
            )
            popular_categories = Category.objects.filter(id__in=pop_cat_ids) if pop_cat_ids else Category.objects.order_by('?')[:5]

            pop_prod_ids = (
                UserVisit.objects
                .values('product')
                .annotate(visits=Count('id'))
                .order_by('-visits')
                .values_list('product', flat=True)[:10]
            )
            popular_products = Product.objects.filter(id__in=pop_prod_ids) if pop_prod_ids else Product.objects.order_by('?')[:10]

        # Optional: Search GIF
        gif = SearchGif.objects.first()
        gif_url = gif.image.url if gif else None

        data = {
            "gif": gif_url,
            "suggested_categories": CategoryNameSerializer(suggested_categories, many=True).data,
            "popular_categories": CategoryNameSerializer(popular_categories, many=True).data,
            "suggested_products": PopularProductSerializer(suggested_products, many=True).data,
            "popular_products": PopularProductSerializer(popular_products, many=True).data,
        }

        return Response(data)



class SearchGifAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk=None):
        if pk:
            try:
                gif = SearchGif.objects.get(pk=pk)
            except SearchGif.DoesNotExist:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = SearchGifSerializer(gif)
            return Response(serializer.data)
        else:
            gifs = SearchGif.objects.all()
            serializer = SearchGifSerializer(gifs, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = SearchGifSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            gif = SearchGif.objects.get(pk=pk)
        except SearchGif.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SearchGifSerializer(gif, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            gif = SearchGif.objects.get(pk=pk)
        except SearchGif.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        gif.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)










class SendOTP(APIView):
    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']

            if Register.objects.filter(username=phone).exists():
                return Response({'error': 'Superuser login not allowed via OTP.'}, status=status.HTTP_403_FORBIDDEN)

            otp = str(random.randint(100000, 999999))

            otp_obj, _ = PhoneOTP.objects.update_or_create(
                phone=phone,
                defaults={'otp': otp, 'is_verified': False}
            )

            send_otp_via_sms(phone, otp)
            return Response({'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





import uuid

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.shortcuts import get_object_or_404
class VerifyOTP(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        otp = request.data.get("otp")

        if not phone or not otp:
            return Response({"error": "Phone and OTP are required"}, status=HTTP_400_BAD_REQUEST)

        try:
            otp_obj = PhoneOTP.objects.get(phone=phone, otp=otp, is_verified=False)
        except PhoneOTP.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=HTTP_400_BAD_REQUEST)

        # Mark OTP as used
        otp_obj.is_verified = True
        otp_obj.save()

        # Create or get user
        user, created = Register.objects.get_or_create(
            mobile=phone,
            defaults={
                "username": f"user_{phone[-4:]}",   # default username
                "password": "otp_auth"              # placeholder password
            }
        )

        # ✅ Create or get UserProfile
        profile, profile_created = UserProfile.objects.get_or_create(
            username=user,   # or use user=user if you rename the field
            defaults={
                "phone_number": phone
            }
        )

        # Generate JWT token
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Account created and login successful" if created else "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": str(user.id),
            "username": user.username,
            "mobile": user.mobile,
            "profile_id": str(profile.id),
            "profile_created": profile_created
        }, status=HTTP_200_OK)



# class AdminLoginAPIView(APIView):
#     def post(self, request):
#         serializer = AdminLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             admin = serializer.validated_data['admin']

#             # Create JWT tokens
#             refresh = RefreshToken.for_user(admin)

#             return Response({
#                 "message": "Login successful",
#                 "username": admin.username,
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#             })
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AdminLoginAPIView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.validated_data['admin']

            # Create custom refresh token
            refresh = RefreshToken()
            refresh['admin_id'] = str(admin.id)
            refresh['username'] = admin.username
            refresh['is_admin'] = True  # Custom claim

            return Response({
                "message": "Admin login successful",
                "username": admin.username,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


import os
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, login
from dotenv import load_dotenv
from rest_framework_simplejwt.tokens import RefreshToken
load_dotenv()
# load_dotenv()
# User = get_user_model()

# @csrf_exempt
# def google_login_callback(request):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Only POST allowed'}, status=405)

#     try:
#         data = json.loads(request.body)
#         access_token = data.get('access_token')

#         if not access_token:
#             return JsonResponse({'error': 'Missing access token'}, status=400)

#         # Get user info from Google
#         userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
#         response = requests.get(
#             userinfo_url,
#             headers={"Authorization": f"Bearer {access_token}"}
#         )

#         if response.status_code != 200:
#             return JsonResponse({'error': 'Failed to fetch user info'}, status=400)

#         user_info = response.json()
#         email = user_info.get("email")
#         name = user_info.get("name")

#         if not email:
#             return JsonResponse({'error': 'Email not returned by Google'}, status=400)

#         # Generate dummy mobile number (e.g., use part of hash or timestamp)
#         dummy_mobile = int("91" + str(abs(hash(email)))[0:8])  # ensures uniqueness

#         # Get or create the user using username=email
#         user, created = User.objects.get_or_create(
#             username=email,
#             defaults={"mobile": dummy_mobile}
#         )

#         login(request, user)

#         refresh = RefreshToken.for_user(user)

#         return JsonResponse({
#             'message': 'Login successful',
#             'username': user.username,
#             'access': str(refresh.access_token),
#             'refresh': str(refresh)
#         })

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)


User = get_user_model()

@csrf_exempt
def google_login_callback(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        access_token = data.get('access_token')

        if not access_token:
            return JsonResponse({'error': 'Missing access token'}, status=400)

        # Get user info from Google
        userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        response = requests.get(
            userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if response.status_code != 200:
            return JsonResponse({'error': 'Failed to fetch user info'}, status=400)

        user_info = response.json()
        email = user_info.get("email")
        name = user_info.get("name")
        # picture = user_info.get("picture")  # optional

        if not email:
            return JsonResponse({'error': 'Email not returned by Google'}, status=400)

        # Generate dummy mobile number using email hash
        dummy_mobile = int("91" + str(abs(hash(email)))[0:8])

        # Create or get user
        user, created = User.objects.get_or_create(
            username=email,
            defaults={"mobile": dummy_mobile}
        )

        # ✅ Create UserProfile if it doesn't exist
        if not hasattr(user, 'profile'):
            try:
                UserProfile.objects.create(
                    username=user,
                    full_name=name,
                    email=email,
                    phone_number=dummy_mobile
                )
                print(f"✅ Created UserProfile for {user.username}")
            except Exception as profile_error:
                print("❌ Failed to create UserProfile:", profile_error)

        # Log in the user
        login(request, user)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            'message': 'Login successful',
            'username': user.username,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)