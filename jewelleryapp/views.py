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

# class ProductListCreateAPIView(APIView):
#     authentication_classes = [CombinedJWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         user = request.user
#         classic_qs = Product.objects.filter(is_classic=True)
#         other_qs   = Product.objects.filter(is_classic=False)

#         context = {'request': request}
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
#             data['ar_model_glb'] = f"https://res.cloudinary.com/YOUR_CLOUD_NAME/raw/upload/v{glb['version']}/{glb['public_id']}"

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
        other_qs = Product.objects.filter(is_classic=False)

        context = {'request': request}
        classic_data = ProductSerializer(classic_qs, many=True, context=context).data
        other_data = ProductSerializer(other_qs, many=True, context=context).data

        return Response({
            "classic_products": classic_data,
            "other_products": other_data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        images = request.FILES.getlist('images')
        image_urls = []

        try:
            for image in images[:5]:
                res = uploader.upload(image)
                image_urls.append(res["secure_url"])
        except Exception as e:
            return Response({"error": f"Image upload failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = {k: v for k, v in request.data.items() if not hasattr(v, 'read')}
        data['images'] = image_urls

        cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME", "dvllntzo0")  # fallback to default if not found

        if 'ar_model_glb' in request.FILES:
            glb = uploader.upload(request.FILES['ar_model_glb'], resource_type='raw')
            data['ar_model_glb'] = f"https://res.cloudinary.com/{cloud_name}/raw/upload/v{glb['version']}/{glb['public_id']}"

        if 'ar_model_gltf' in request.FILES:
            gltf = uploader.upload(request.FILES['ar_model_gltf'], resource_type='raw')
            data['ar_model_gltf'] = gltf['secure_url']

        serializer = ProductSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProductDetailAPIView(APIView):
#     authentication_classes = [CombinedJWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_object(self, pk):
#         try:
#             return Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             raise NotFound("Product not found")

#     def get(self, request, pk, *args, **kwargs):
#         product = self.get_object(pk)
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)

#     def put(self, request, pk, *args, **kwargs):
#         product = self.get_object(pk)
#         data = dict(request.data)

#         # ✅ Handle multiple image uploads (up to 5)
#         new_images = request.FILES.getlist('images')
#         if new_images:
#             uploaded_images = []
#             try:
#                 for image in new_images[:5]:
#                     upload_result = uploader.upload(image)
#                     uploaded_images.append(upload_result["secure_url"])
#                 data['images'] = json.dumps(uploaded_images)
#             except Exception as e:
#                 return Response({"error": f"Image upload failed: {str(e)}"}, status=500)
#         else:
#             data.pop('images', None)

#         # ✅ Handle AR model GLB
#         if 'ar_model_glb' in request.FILES:
#             glb_upload = uploader.upload(request.FILES['ar_model_glb'], resource_type='raw')
#             data['ar_model_glb'] = f"https://res.cloudinary.com/dvllntzo0/raw/upload/v{glb_upload['version']}/{glb_upload['public_id']}"

#         # ✅ Handle AR model GLTF
#         if 'ar_model_gltf' in request.FILES:
#             gltf_upload = uploader.upload(request.FILES['ar_model_gltf'], resource_type='raw')
#             data['ar_model_gltf'] = gltf_upload['secure_url']

#         # ✅ Parse JSON string for 'images' if needed
#         if 'images' in data and isinstance(data['images'], str):
#             try:
#                 data['images'] = json.loads(data['images'])
#             except json.JSONDecodeError:
#                 return Response({"images": ["Value must be valid JSON."]}, status=400)

#         messages = []

#         # ✅ Handle stock increment
#         if 'total_stock' in data:
#             try:
#                 stock_value = data['total_stock'][0] if isinstance(data['total_stock'], list) else data['total_stock']
#                 added_stock = int(stock_value)
#                 product.total_stock += added_stock
#                 product.save()
#                 messages.append(f"Added {added_stock} to stock.")
#             except ValueError:
#                 return Response({"total_stock": ["A valid integer is required."]}, status=400)
#             data.pop('total_stock')

#         # ✅ Handle sold_count increment
#         if 'sold_count' in data:
#             try:
#                 sold_value = data['sold_count'][0] if isinstance(data['sold_count'], list) else data['sold_count']
#                 sold_increment = int(sold_value)
#                 if sold_increment < 0:
#                     return Response({"sold_count": ["Sold count cannot be negative."]}, status=400)

#                 available_stock = product.total_stock - product.sold_count
#                 if sold_increment > available_stock:
#                     return Response({
#                         "message": "Not enough stock to sell.",
#                         "product": ProductSerializer(product).data
#                     }, status=400)

#                 product.sold_count += sold_increment
#                 product.save()
#                 messages.append(f"{sold_increment} items sold.")
#             except ValueError:
#                 return Response({"sold_count": ["A valid integer is required."]}, status=400)
#             data.pop('sold_count')

#         # ✅ Save changes
#         serializer = ProductSerializer(product, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "message": " ".join(messages) or "Product updated successfully.",
#                 "product": serializer.data
#             })

#         return Response(serializer.errors, status=400)



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

        # ✅ Parse JSON string for 'images'
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

    def delete(self, request, pk, *args, **kwargs):
        """
        Delete the product.
        """
        product = self.get_object(pk)
        product.delete()
        return Response({"message": f"Product '{product.head}' deleted successfully."}, status=status.HTTP_204_NO_CONTENT)






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
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]
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
# class OccasionListCreateAPIView(BaseListCreateAPIView):
#     model = Occasion
#     serializer_class = OccasionSerializer


class OccasionListCreateAPIView(APIView):
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        occasions = Occasion.objects.all()
        serializer = OccasionSerializer(occasions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OccasionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        occasion_id = request.data.get("id")
        if not occasion_id:
            return Response({"error": "ID is required to delete."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            occasion = Occasion.objects.get(id=occasion_id)
            occasion.delete()
            return Response({"message": "Occasion deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Occasion.DoesNotExist:
            return Response({"error": "Occasion not found."}, status=status.HTTP_404_NOT_FOUND)


# class OccasionDetailAPIView(BaseDetailAPIView):
#     model = Occasion
#     serializer_class = OccasionSerializer


class OccasionDetailAPIView(APIView):
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


    def get(self, request, pk):
        occasion = get_object_or_404(Occasion, pk=pk)
        serializer = OccasionSerializer(occasion)
        return Response(serializer.data)

    def put(self, request, pk):
        occasion = get_object_or_404(Occasion, pk=pk)

        # Make request data mutable
        data = request.data.copy()

        # Get actual list of serializer fields
        serializer_fields = OccasionSerializer().get_fields()

        # Preserve existing values for fields not in the request
        for field in serializer_fields:
            if field not in data:
                value = getattr(occasion, field)
                if field == 'image' and value:
                    data[field] = value  # ImageField needs special care
                elif value is not None:
                    data[field] = value

        serializer = OccasionSerializer(occasion, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        occasion = get_object_or_404(Occasion, pk=pk)
        occasion.delete()
        return Response({"message": "Occasion deleted successfully."}, status=status.HTTP_204_NO_CONTENT)




# class ProductByOccasion(APIView):
#     permission_classes = [AllowAny]

#     def get_filter_data(self, products):
#         grand_totals = [float(p.grand_total) for p in products if p.grand_total is not None]
#         min_price = min(grand_totals) if grand_totals else 0
#         max_price = max(grand_totals) if grand_totals else 0

#         materials = Material.objects.filter(
#             id__in=products.values_list('metal__material_id', flat=True)
#         ).values('id', 'name').distinct()

#         gemstones = Gemstone.objects.filter(
#             productstone__product__in=products
#         ).values('id', 'name').distinct()

#         metal_colors = Metal.objects.filter(
#             id__in=products.values_list('metal_id', flat=True)
#         ).values_list("color", flat=True).distinct()

#         colors_with_codes = []
#         for color in metal_colors:
#             color_name = str(color).strip().lower()
#             try:
#                 hex_code = name_to_hex(color_name)
#             except ValueError:
#                 hex_code = "#CCCCCC"
#             colors_with_codes.append({"color": color, "code": hex_code})

#         subcategories = Subcategories.objects.filter(
#             category__in=products.values_list('category_id', flat=True)
#         ).values("id", "sub_name").distinct()

#         categories = products.values('category__id', 'category__name').distinct()
#         category_list = [{"id": c["category__id"], "name": c["category__name"]} for c in categories]

#         return {
#             "price_range": {"min": min_price, "max": max_price},
#             "materials": list(materials),
#             "gemstones": list(gemstones),
#             "colors": colors_with_codes,
#             "subcategories": list(subcategories),
#             "categories": category_list,
#             "brand": "my jewelry my design"
#         }

#     def filter_products(self, products, data):
#         price_min = price_max = None

#         def parse_list(field):
#             if hasattr(data, 'getlist'):
#                 return [v for v in data.getlist(field) if v]
#             val = data.get(field)
#             return [val] if val else []

#         subcategories = parse_list('subcategory')
#         materials = parse_list('materials')
#         gemstones = parse_list('gemstones')
#         colors = parse_list('colors')
#         brand = data.get('brand')
#         price_raw = data.get('price')

#         try:
#             if isinstance(price_raw, str) and "-" in price_raw:
#                 price_min, price_max = map(float, price_raw.split("-"))
#             elif isinstance(price_raw, dict):
#                 price_min = float(price_raw.get("min", 0))
#                 price_max = float(price_raw.get("max", 1000000))
#             elif isinstance(price_raw, str) and price_raw.strip().startswith("{"):
#                 price_dict = json.loads(price_raw)
#                 price_min = float(price_dict.get("min", 0))
#                 price_max = float(price_dict.get("max", 1000000))
#         except (ValueError, TypeError, json.JSONDecodeError):
#             price_min = price_max = None

#         if subcategories:
#             products = products.filter(Subcategories__sub_name__in=subcategories)
#         if brand:
#             products = products.filter(head__icontains=brand)
#         if materials:
#             products = products.filter(metal__material__name__in=materials)
#         if gemstones:
#             products = products.filter(productstone__stone__name__in=gemstones).distinct()
#         if colors:
#             products = products.filter(metal__color__in=colors)

#         filtered = []
#         for product in products:
#             try:
#                 grand_total = float(product.grand_total)
#             except Exception:
#                 continue

#             if price_min is not None and price_max is not None:
#                 if grand_total < price_min or grand_total > price_max:
#                     continue
#             filtered.append(product)

#         return filtered

#     def get(self, request, pk, *args, **kwargs):
#         occasion = get_object_or_404(Occasion, pk=pk)
#         products = Product.objects.filter(occasion=occasion)

#         product_list = [{
#             "id": p.id,
#             "head": p.head,
#             "description": p.description,
#             "first_image": p.images[0] if p.images else None,
#             "average_rating": p.average_rating,
#             "grand_total": str(p.grand_total),
#             "is_wishlisted": True  # Replace with your wishlist logic
#         } for p in products]

#         filter_data = self.get_filter_data(products)

#         return Response({
#             "occasion": {
#                 "id": occasion.id,
#                 "name": occasion.name
#             },
#             "products": product_list,
#             "filter_occasion": [filter_data],
#         })

#     def post(self, request, pk, *args, **kwargs):
#         occasion = get_object_or_404(Occasion, pk=pk)
#         clear_filter = request.data.get('clear', False)

#         products = Product.objects.filter(occasion=occasion)
#         if not clear_filter:
#             products = self.filter_products(products, request.data)

#         product_list = [{
#             "id": p.id,
#             "head": p.head,
#             "description": p.description,
#             "first_image": p.images[0] if p.images else None,
#             "average_rating": p.average_rating,
#             "grand_total": str(p.grand_total),
#             "is_wishlisted": True  # Replace with your wishlist logic
#         } for p in products]

#         filter_data = self.get_filter_data(Product.objects.filter(occasion=occasion))

#         message = None
#         if not clear_filter:
#             message = "Filters Applied" if product_list else "No Matching Filters"

#         response = {
#             "occasion": {
#                 "id": occasion.id,
#                 "name": occasion.name
#             },
#             "products": product_list,
#             "filter_occasion": [filter_data],
#         }
#         if message:
#             response["message"] = message

#         return Response(response)


# class ProductByOccasion(APIView):
#     permission_classes = [AllowAny]

#     def get_filter_data(self, products):
#         grand_totals = [float(p.grand_total) for p in products if p.grand_total is not None]
#         min_price = min(grand_totals) if grand_totals else 0
#         max_price = max(grand_totals) if grand_totals else 0

#         materials = Material.objects.filter(
#             id__in=products.values_list('metal__material_id', flat=True)
#         ).values('id', 'name').distinct()

#         gemstones = Gemstone.objects.filter(
#             productstone__product__in=products
#         ).values('id', 'name').distinct()

#         metal_colors = Metal.objects.filter(
#             id__in=products.values_list('metal_id', flat=True)
#         ).values_list("color", flat=True).distinct()

#         colors_with_codes = []
#         for color in metal_colors:
#             color_name = str(color).strip().lower()
#             try:
#                 hex_code = name_to_hex(color_name)
#             except ValueError:
#                 hex_code = "#CCCCCC"
#             colors_with_codes.append({"color": color, "code": hex_code})

#         categories = products.values('category__id', 'category__name').distinct()
#         category_list = [{"id": c["category__id"], "name": c["category__name"]} for c in categories]

#         return {
#             "price_range": {"min": min_price, "max": max_price},
#             "materials": list(materials),
#             "gemstones": list(gemstones),
#             "colors": colors_with_codes,
#             "categories": category_list,
#             "brand": "my jewelry my design"
#         }

#     def filter_products(self, products, data):
#         price_min = price_max = None

#         def parse_list(field):
#             if hasattr(data, 'getlist'):
#                 return [v for v in data.getlist(field) if v]
#             val = data.get(field)
#             return [val] if val else []

#         # Removed subcategories filter here
#         materials = parse_list('materials')
#         gemstones = parse_list('gemstones')
#         colors = parse_list('colors')
#         brand = data.get('brand')
#         price_raw = data.get('price')

#         try:
#             if isinstance(price_raw, str) and "-" in price_raw:
#                 price_min, price_max = map(float, price_raw.split("-"))
#             elif isinstance(price_raw, dict):
#                 price_min = float(price_raw.get("min", 0))
#                 price_max = float(price_raw.get("max", 1000000))
#             elif isinstance(price_raw, str) and price_raw.strip().startswith("{"):
#                 price_dict = json.loads(price_raw)
#                 price_min = float(price_dict.get("min", 0))
#                 price_max = float(price_dict.get("max", 1000000))
#         except (ValueError, TypeError, json.JSONDecodeError):
#             price_min = price_max = None

#         if brand:
#             products = products.filter(head__icontains=brand)
#         if materials:
#             products = products.filter(metal__material__name__in=materials)
#         if gemstones:
#             products = products.filter(productstone__stone__name__in=gemstones).distinct()
#         if colors:
#             products = products.filter(metal__color__in=colors)

#         filtered = []
#         for product in products:
#             try:
#                 grand_total = float(product.grand_total)
#             except Exception:
#                 continue

#             if price_min is not None and price_max is not None:
#                 if grand_total < price_min or grand_total > price_max:
#                     continue
#             filtered.append(product)

#         return filtered

#     def get(self, request, pk, *args, **kwargs):
#         occasion = get_object_or_404(Occasion, pk=pk)
#         products = Product.objects.filter(occasion=occasion)

#         product_list = [{
#             "id": p.id,
#             "head": p.head,
#             "description": p.description,
#             "first_image": p.images[0] if p.images else None,
#             "average_rating": p.average_rating,
#             "grand_total": str(p.grand_total),
#             "is_wishlisted": True  # Replace with your wishlist logic
#         } for p in products]

#         filter_data = self.get_filter_data(products)

#         return Response({
#             "occasion": {
#                 "id": occasion.id,
#                 "name": occasion.name
#             },
#             "products": product_list,
#             "filter_occasion": [filter_data],
#         })

#     def post(self, request, pk, *args, **kwargs):
#         occasion = get_object_or_404(Occasion, pk=pk)
#         clear_filter = request.data.get('clear', False)

#         products = Product.objects.filter(occasion=occasion)
#         if not clear_filter:
#             products = self.filter_products(products, request.data)

#         product_list = [{
#             "id": p.id,
#             "head": p.head,
#             "description": p.description,
#             "first_image": p.images[0] if p.images else None,
#             "average_rating": p.average_rating,
#             "grand_total": str(p.grand_total),
#             "is_wishlisted": True  # Replace with your wishlist logic
#         } for p in products]

#         filter_data = self.get_filter_data(Product.objects.filter(occasion=occasion))

#         message = None
#         if not clear_filter:
#             message = "Filters Applied" if product_list else "No Matching Filters"

#         response = {
#             "occasion": {
#                 "id": occasion.id,
#                 "name": occasion.name
#             },
#             "products": product_list,
#             "filter_occasion": [filter_data],
#         }
#         if message:
#             response["message"] = message

#         return Response(response)

# class ProductByOccasion(APIView):
#     permission_classes = [AllowAny]

#     def get_filter_data(self, products):
#         grand_totals = [float(p.grand_total) for p in products if p.grand_total is not None]
#         min_price = min(grand_totals) if grand_totals else 0
#         max_price = max(grand_totals) if grand_totals else 0

#         materials = Material.objects.filter(
#             id__in=products.values_list('metal__material_id', flat=True)
#         ).values('id', 'name').distinct()

#         gemstones = Gemstone.objects.filter(
#             productstone__product__in=products
#         ).values('id', 'name').distinct()

#         metal_colors = Metal.objects.filter(
#             id__in=products.values_list('metal_id', flat=True)
#         ).values_list("color", flat=True).distinct()

#         colors_with_codes = []
#         for color in metal_colors:
#             color_name = str(color).strip().lower()
#             try:
#                 hex_code = name_to_hex(color_name)
#             except ValueError:
#                 hex_code = "#CCCCCC"
#             colors_with_codes.append({"color": color, "code": hex_code})

#         categories = products.values('category__id', 'category__name').distinct()
#         category_list = [{"id": c["category__id"], "name": c["category__name"]} for c in categories]

#         return {
#             "price_range": {"min": min_price, "max": max_price},
#             "materials": list(materials),
#             "gemstones": list(gemstones),
#             "colors": colors_with_codes,
#             "categories": category_list,
#             "brand": "my jewelry my design"
#         }

#     def filter_products(self, products, data):
#         price_min = price_max = None

#         def parse_list(field):
#             if hasattr(data, 'getlist'):
#                 return [v for v in data.getlist(field) if v]
#             val = data.get(field)
#             return [val] if val else []

#         categories = parse_list('categories')  # New filter key for categories
#         materials = parse_list('materials')
#         gemstones = parse_list('gemstones')
#         colors = parse_list('colors')
#         brand = data.get('brand')
#         price_raw = data.get('price')

#         try:
#             if isinstance(price_raw, str) and "-" in price_raw:
#                 price_min, price_max = map(float, price_raw.split("-"))
#             elif isinstance(price_raw, dict):
#                 price_min = float(price_raw.get("min", 0))
#                 price_max = float(price_raw.get("max", 1000000))
#             elif isinstance(price_raw, str) and price_raw.strip().startswith("{"):
#                 price_dict = json.loads(price_raw)
#                 price_min = float(price_dict.get("min", 0))
#                 price_max = float(price_dict.get("max", 1000000))
#         except (ValueError, TypeError, json.JSONDecodeError):
#             price_min = price_max = None

#         if brand:
#             products = products.filter(head__icontains=brand)
#         if categories:
#             # convert category IDs to integers, just in case
#             try:
#                 category_ids = [int(cat) for cat in categories]
#                 products = products.filter(category__id__in=category_ids)
#             except ValueError:
#                 pass  # Ignore invalid category IDs
#         if materials:
#             products = products.filter(metal__material__name__in=materials)
#         if gemstones:
#             products = products.filter(productstone__stone__name__in=gemstones).distinct()
#         if colors:
#             products = products.filter(metal__color__in=colors)

#         filtered = []
#         for product in products:
#             try:
#                 grand_total = float(product.grand_total)
#             except Exception:
#                 continue

#             if price_min is not None and price_max is not None:
#                 if grand_total < price_min or grand_total > price_max:
#                     continue
#             filtered.append(product)

#         return filtered

#     def get(self, request, pk, *args, **kwargs):
#         occasion = get_object_or_404(Occasion, pk=pk)
#         products = Product.objects.filter(occasion=occasion)

#         product_list = [{
#             "id": p.id,
#             "head": p.head,
#             "description": p.description,
#             "first_image": p.images[0] if p.images else None,
#             "average_rating": p.average_rating,
#             "grand_total": str(p.grand_total),
#             "is_wishlisted": True  # Replace with your wishlist logic
#         } for p in products]

#         filter_data = self.get_filter_data(products)

#         return Response({
#             "occasion": {
#                 "id": occasion.id,
#                 "name": occasion.name
#             },
#             "products": product_list,
#             "filter_occasion": [filter_data],
#         })

#     def post(self, request, pk, *args, **kwargs):
#         occasion = get_object_or_404(Occasion, pk=pk)
#         clear_filter = request.data.get('clear', False)

#         products = Product.objects.filter(occasion=occasion)
#         if not clear_filter:
#             products = self.filter_products(products, request.data)

#         product_list = [{
#             "id": p.id,
#             "head": p.head,
#             "description": p.description,
#             "first_image": p.images[0] if p.images else None,
#             "average_rating": p.average_rating,
#             "grand_total": str(p.grand_total),
#             "is_wishlisted": True  # Replace with your wishlist logic
#         } for p in products]

#         filter_data = self.get_filter_data(Product.objects.filter(occasion=occasion))

#         message = None
#         if not clear_filter:
#             message = "Filters Applied" if product_list else "No Matching Filters"

#         response = {
#             "occasion": {
#                 "id": occasion.id,
#                 "name": occasion.name
#             },
#             "products": product_list,
#             "filter_occasion": [filter_data],
#         }
#         if message:
#             response["message"] = message

#         return Response(response)
class ProductByOccasion(APIView):
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_filter_data(self, products):
        grand_totals = [float(p.grand_total) for p in products if p.grand_total is not None]
        min_price = min(grand_totals) if grand_totals else 0
        max_price = max(grand_totals) if grand_totals else 0

        materials = Material.objects.filter(
            id__in=products.values_list('metal__material_id', flat=True)
        ).values('id', 'name').distinct()

        gemstones = Gemstone.objects.filter(
            productstone__product__in=products
        ).values('id', 'name').distinct()

        metal_colors = Metal.objects.filter(
            id__in=products.values_list('metal_id', flat=True)
        ).values_list("color", flat=True).distinct()

        colors_with_codes = []
        for color in metal_colors:
            color_name = str(color).strip().lower()
            try:
                hex_code = name_to_hex(color_name)
            except ValueError:
                hex_code = "#CCCCCC"
            colors_with_codes.append({"color": color, "code": hex_code})

        categories = products.values_list('category__name', flat=True).distinct()
        category_list = list(categories)

        return {
            "price_range": {"min": min_price, "max": max_price},
            "metal": list(materials),
            "gemstone": list(gemstones),
            "colors": colors_with_codes,
            "category": category_list,
            "brand": "my jewelry my design"
        }

    def filter_products(self, products, data):
        price_min = price_max = None

        def parse_list(field):
            if hasattr(data, 'getlist'):
                return [v for v in data.getlist(field) if v]
            val = data.get(field)
            return [val] if val else []

        category = parse_list('category')
        metal = parse_list('metal')
        gemstone = parse_list('gemstone')
        colors = parse_list('colors')
        brand = data.get('brand')
        price_raw = data.get('price')

        try:
            if isinstance(price_raw, str) and "-" in price_raw:
                price_min, price_max = map(float, price_raw.split("-"))
            elif isinstance(price_raw, dict):
                price_min = float(price_raw.get("min", 0))
                price_max = float(price_raw.get("max", 1000000))
            elif isinstance(price_raw, str) and price_raw.strip().startswith("{"):
                price_dict = json.loads(price_raw)
                price_min = float(price_dict.get("min", 0))
                price_max = float(price_dict.get("max", 1000000))
        except (ValueError, TypeError, json.JSONDecodeError):
            price_min = price_max = None

        if brand:
            products = products.filter(head__icontains=brand)
        if category:
            products = products.filter(category__name__in=category)
        if metal:
            products = products.filter(metal__material__name__in=metal)
        if gemstone:
            products = products.filter(productstone__stone__name__in=gemstone).distinct()
        if colors:
            products = products.filter(metal__color__in=colors)

        filtered = []
        for product in products:
            try:
                grand_total = float(product.grand_total)
                if price_min is not None and price_max is not None:
                    if grand_total < price_min or grand_total > price_max:
                        continue
                filtered.append(product)
            except Exception:
                continue

        return filtered

    def get(self, request, pk, *args, **kwargs):
        occasion = get_object_or_404(Occasion, pk=pk)
        products = Product.objects.filter(occasion=occasion)

        # Fetch wishlisted IDs based on filtered product IDs
        product_ids = list(products.values_list("id", flat=True))
        wishlisted_ids = set()
        if request.user.is_authenticated:
            wishlisted_ids = set(
                Wishlist.objects.filter(user=request.user, product_id__in=product_ids)
                .values_list('product_id', flat=True)
            )

        product_list = [{
            "id": p.id,
            "head": p.head,
            "description": p.description,
            "first_image": p.images[0] if p.images else None,
            "average_rating": p.average_rating,
            "grand_total": str(p.grand_total),
            "is_wishlisted": p.id in wishlisted_ids
        } for p in products]

        filter_data = self.get_filter_data(products)

        return Response({
           "category":occasion.name,
            "products": product_list,
            "filter_category": [filter_data],
        })

    def post(self, request, pk, *args, **kwargs):
        occasion = get_object_or_404(Occasion, pk=pk)
        clear_filter = request.data.get('clear', False)

        products = Product.objects.filter(occasion=occasion)
        if not clear_filter:
            products = self.filter_products(products, request.data)

        product_ids = list(products.values_list("id", flat=True))
        wishlisted_ids = set()
        if request.user.is_authenticated:
            wishlisted_ids = set(
                Wishlist.objects.filter(user=request.user, product_id__in=product_ids)
                .values_list('product_id', flat=True)
            )

        product_list = [{
            "id": p.id,
            "head": p.head,
            "description": p.description,
            "first_image": p.images[0] if p.images else None,
            "average_rating": p.average_rating,
            "grand_total": str(p.grand_total),
            "is_wishlisted": p.id in wishlisted_ids
        } for p in products]

        filter_data = self.get_filter_data(Product.objects.filter(occasion=occasion))

        message = None
        if not clear_filter:
            message = "Filters Applied" if product_list else "No Matching Filters"

        response = {
            "occasion": {
                "id": occasion.id,
                "name": occasion.name
            },
            "products": product_list,
            "filter_occasion": [filter_data],
        }
        if message:
            response["message"] = message

        return Response(response)

class PriceRangeLabelsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        price_ranges = [
            {
                "id": 1,
                "label": "Below 25K",
                "min_price": 0,
                "max_price": 25000
            },
            {
                "id": 2,
                "label": "25K - 50K",
                "min_price": 25000,
                "max_price": 50000
            },
            {
                "id": 3,
                "label": "50K - 1L",
                "min_price": 50000,
                "max_price": 100000
            },
            {
                "id": 4,
                "label": "Above 1L",
                "min_price": 100000,
                "max_price": None
            }
        ]
        return Response({"price_ranges": price_ranges})
    

from django.db.models import F, ExpressionWrapper, DecimalField
# class ProductByPriceRangeAPIView(APIView):
#     def post(self, request):
#         price_id = request.data.get("price_id")

#         if not price_id:
#             return Response({"error": "price_id is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             price_id = int(price_id)
#         except ValueError:
#             return Response({"error": "Invalid price_id."}, status=status.HTTP_400_BAD_REQUEST)

#         # Define ranges based on the same labels used in MegaNavbar
#         price_ranges = {
#             1: {"min": Decimal("0.00"), "max": Decimal("25000.00")},
#             2: {"min": Decimal("25000.01"), "max": Decimal("50000.00")},
#             3: {"min": Decimal("50000.01"), "max": Decimal("100000.00")},
#             4: {"min": Decimal("100000.01"), "max": None},  # 1L & above
#         }

#         selected_range = price_ranges.get(price_id)
#         if not selected_range:
#             return Response({"error": "Invalid price_id."}, status=status.HTTP_400_BAD_REQUEST)

#         # Filter products by grand_total
#         products = Product.objects.all()
#         filtered_products = []
#         for product in products:
#             if product.grand_total is None:
#                 continue
#             price = product.grand_total
#             if selected_range["max"] is None:
#                 if price >= selected_range["min"]:
#                     filtered_products.append(product)
#             elif selected_range["min"] <= price <= selected_range["max"]:
#                 filtered_products.append(product)

#         serializer = ProductSerializer(filtered_products, many=True, context={"request": request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
# class PriceRangeProductAPIView(APIView):
#     """
#     GET: /api/products/by-price-range/?range_id=1
#     Returns products filtered by predefined price range.
#     """

#     def get_price_range(self, range_id):
#         """
#         Maps static range_id to min and max prices.
#         """
#         price_map = {
#             1: (0, 25000),
#             2: (25000, 50000),
#             3: (50000, 100000),
#             4: (100000, None),  # 1L & above
#         }
#         return price_map.get(range_id, (None, None))

#     def get(self, request):
#         try:
#             range_id = int(request.GET.get('range_id'))
#         except (TypeError, ValueError):
#             return Response({"detail": "Invalid or missing range_id"}, status=400)

#         min_price, max_price = self.get_price_range(range_id)
#         if min_price is None:
#             return Response({"detail": "Invalid range_id"}, status=400)

#         products = Product.objects.all()
#         filtered_products = []

#         for product in products:
#             if product.grand_total is None:
#                 continue

#             price = float(product.grand_total)

#             if (min_price is not None and price < min_price):
#                 continue
#             if (max_price is not None and price >= max_price):
#                 continue

#             filtered_products.append(product)

#         serializer = ProductSerializer(filtered_products, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)




# class PriceRangeProductAPIView(APIView):
#     """
#     GET: /api/products/by-price-range/?range_id=1&category=1&metal=Gold&gemstone=Ruby
#     Returns products filtered by predefined price range and optional dynamic filters,
#     along with filter options and dynamic price range.
#     """

#     def get_price_range(self, range_id):
#         price_map = {
#             1: (0, 25000),
#             2: (25000, 50000),
#             3: (50000, 100000),
#             4: (100000, None),  # 1L & above
#         }
#         return price_map.get(range_id, (None, None))

#     def get(self, request):
#         try:
#             range_id = int(request.GET.get("range_id"))
#         except (TypeError, ValueError):
#             return Response({"detail": "Invalid or missing range_id"}, status=400)

#         min_price, max_price = self.get_price_range(range_id)
#         if min_price is None:
#             return Response({"detail": "Invalid range_id"}, status=400)

#         # Dynamic filters
#         category = request.GET.get("category")
#         metal = request.GET.get("metal")
#         gemstone = request.GET.get("gemstone")

#         products = Product.objects.all()

#         if category:
#             products = products.filter(category_id=category)
#         if metal:
#             products = products.filter(metal__name__iexact=metal)
#         if gemstone:
#             products = products.filter(stones__name__iexact=gemstone)

#         filtered_products = []
#         prices = []

#         for product in products:
#             price = float(product.grand_total or 0)
#             if (min_price is not None and price < min_price) or \
#                (max_price is not None and price >= max_price):
#                 continue

#             prices.append(price)

#             filtered_products.append({
#                 "id": product.id,
#                 "unit_price": str(product.frozen_unit_price or product.metal.unit_price),
#                 "value": str((product.metal_weight * (product.frozen_unit_price or product.metal.unit_price)).quantize(Decimal('0.001'))),
#                 "items": [
#                     {
#                         "type": "product",
#                         "name": product.metal.name,
#                         "subLabel": f"{product.karat}KT" if product.karat else "",
#                         "rate": f"₹ {(product.frozen_unit_price or product.metal.unit_price):.2f}/g",
#                         "weight": f"{product.metal_weight}g",
#                         "discount": "_",
#                         "value": f"₹ {(product.metal_weight * (product.frozen_unit_price or product.metal.unit_price)).quantize(Decimal('0.01'))}",
#                         "image": product.images[0] if product.images else ""
#                     },
#                     {
#                         "type": "charges",
#                         "label": "Making Charges",
#                         "rate": "_",
#                         "weight": "_",
#                         "discount": "-",
#                         "value": f"₹ {product.making_charge:.2f}"
#                     },
#                     {
#                         "type": "subtotal",
#                         "label": "Sub Total",
#                         "rate": "_",
#                         "weight": f"{product.metal_weight}g Gross Wt.",
#                         "discount": "-",
#                         "value": f"₹ {product.subtotal:.2f}"
#                     },
#                     {
#                         "type": "gst",
#                         "label": "GST",
#                         "rate": "",
#                         "weight": "_",
#                         "discount": "-",
#                         "value": f"₹ {(product.subtotal * (product.gst / 100)).quantize(Decimal('0.01'))}"
#                     },
#                     {
#                         "type": "charges",
#                         "label": "Grand Total",
#                         "rate": "_",
#                         "weight": "_",
#                         "discount": "-",
#                         "value": f"₹ {product.grand_total:.2f}"
#                     }
#                 ],
#                 "stone_price_total": str(product.stone_price_total),
#                 "subtotal": str(product.subtotal),
#                 "grand_total": str(product.grand_total),
#                 "stones": [s.name for s in product.stones.all()],
#                 "average_rating": product.average_rating,
#                 "available_stock": product.available_stock,
#                 "stock_message": "Out of stock" if product.available_stock == 0 else "In stock",
#                 "is_wishlisted": False,
#                 "category": product.category.name,
#                 "occasion": product.occasion.name,
#                 "gender": product.gender.name,
#                 "metal": product.metal.name,
#                 "brand": "My Jewellery",
#                 "details": [
#                     {
#                         "title": "Metal Details",
#                         "content": [
#                             {"heading": f"{product.karat}K", "discription": "Karatage"},
#                             {"heading": "Yellow", "discription": "Material Colour"},
#                             {"heading": f"{product.metal_weight}g", "discription": "Gross Weight"},
#                             {"heading": product.metal.name, "discription": "Metal"},
#                         ],
#                     },
#                     {
#                         "title": "General Details",
#                         "content": [
#                             {"heading": "Jewelry", "discription": "Jewellery Type"},
#                             {"heading": "My Jewellery", "discription": "Brand"},
#                             {"heading": "Best Sellers", "discription": "Collection"},
#                             {"heading": product.gender.name, "discription": "Gender"},
#                             {"heading": product.occasion.name, "discription": "Occasion"},
#                         ],
#                     },
#                     {
#                         "title": "Description",
#                         "content": [
#                             {"description": product.description or ""}
#                         ]
#                     }
#                 ],
#                 "head": product.head,
#                 "size": product.size,
#                 "metal_weight": str(product.metal_weight),
#                 "karat": product.karat,
#                 "images": product.images if product.images else [],
#                 "ar_model_glb": product.ar_model_glb,
#                 "ar_model_gltf": product.ar_model_gltf,
#                 "description": product.description,
#                 "pendant_width": product.pendant_width,
#                 "pendant_height": product.pendant_height,
#                 "frozen_unit_price": str(product.frozen_unit_price),
#                 "making_charge": str(product.making_charge),
#                 "making_discount": str(product.making_discount),
#                 "product_discount": str(product.product_discount),
#                 "gst": str(product.gst),
#                 "handcrafted_charge": str(product.handcrafted_charge),
#                 "is_handcrafted": product.is_handcrafted,
#                 "is_classic": product.is_classic,
#                 "designing_charge": str(product.designing_charge),
#                 "total_stock": product.total_stock,
#                 "sold_count": product.sold_count,
#                 "created_at": product.created_at,
#                 "Subcategories": product.Subcategories.id if product.Subcategories else None,
#             })

#         # Final filters data including new 'colors' section
#         filters = {
#             "category": list(Category.objects.values("id", "name")),
#             "metal": list(Metal.objects.values_list("name", flat=True)),
#             "gemstone": list(Gemstone.objects.values_list("name", flat=True)),
#             "brand": "My Jewellery",
#             "colors": [
#                 {
#                     "color": "Yellow",
#                     "code": "#ffff00"
#                 }
#             ]
#         }

#         # Dynamic price range from the filtered results
#         price_range = {
#             "min": min(prices) if prices else None,
#             "max": max(prices) if prices else None
#         }

#         return Response({
#             "products": filtered_products,
#             "filters": filters,
#             "price_range": price_range
#         }, status=status.HTTP_200_OK)


# class PriceRangeProductAPIView(APIView):
#     """
#     GET: /api/products/by-price-range/?range_id=1&category=1&metal=Gold&gemstone=Ruby
#     Returns products filtered by predefined price range and optional dynamic filters,
#     along with filter options and dynamic price range.
#     """

#     def get_price_range(self, range_id):
#         price_map = {
#             1: (0, 25000),
#             2: (25000, 50000),
#             3: (50000, 100000),
#             4: (100000, None),  # 1L & above
#         }
#         return price_map.get(range_id, (None, None))

#     def get(self, request):
#         try:
#             range_id = int(request.GET.get("range_id"))
#         except (TypeError, ValueError):
#             return Response({"detail": "Invalid or missing range_id"}, status=400)

#         min_price, max_price = self.get_price_range(range_id)
#         if min_price is None:
#             return Response({"detail": "Invalid range_id"}, status=400)

#         # Dynamic filters
#         category = request.GET.get("category")
#         metal = request.GET.get("metal")
#         gemstone = request.GET.get("gemstone")

#         products = Product.objects.all()

#         if category:
#             products = products.filter(category_id=category)
#         if metal:
#             products = products.filter(metal__name__iexact=metal)
#         if gemstone:
#             products = products.filter(stones__name__iexact=gemstone)

#         filtered_products = []
#         prices = []

#         for product in products:
#             price = float(product.grand_total or 0)
#             if (min_price is not None and price < min_price) or \
#                (max_price is not None and price >= max_price):
#                 continue

#             prices.append(price)

#             filtered_products.append({
#                 "id": product.id,
#                 "unit_price": str(product.frozen_unit_price or product.metal.unit_price),
#                 "value": str((product.metal_weight * (product.frozen_unit_price or product.metal.unit_price)).quantize(Decimal('0.001'))),
#                 "items": [
#                     {
#                         "type": "product",
#                         "name": product.metal.name,
#                         "subLabel": f"{product.karat}KT" if product.karat else "",
#                         "rate": f"₹ {(product.frozen_unit_price or product.metal.unit_price):.2f}/g",
#                         "weight": f"{product.metal_weight}g",
#                         "discount": "_",
#                         "value": f"₹ {(product.metal_weight * (product.frozen_unit_price or product.metal.unit_price)).quantize(Decimal('0.01'))}",
#                         "image": product.images[0] if product.images else ""
#                     },
#                     {
#                         "type": "charges",
#                         "label": "Making Charges",
#                         "rate": "_",
#                         "weight": "_",
#                         "discount": "-",
#                         "value": f"₹ {product.making_charge:.2f}"
#                     },
#                     {
#                         "type": "subtotal",
#                         "label": "Sub Total",
#                         "rate": "_",
#                         "weight": f"{product.metal_weight}g Gross Wt.",
#                         "discount": "-",
#                         "value": f"₹ {product.subtotal:.2f}"
#                     },
#                     {
#                         "type": "gst",
#                         "label": "GST",
#                         "rate": "",
#                         "weight": "_",
#                         "discount": "-",
#                         "value": f"₹ {(product.subtotal * (product.gst / 100)).quantize(Decimal('0.01'))}"
#                     },
#                     {
#                         "type": "charges",
#                         "label": "Grand Total",
#                         "rate": "_",
#                         "weight": "_",
#                         "discount": "-",
#                         "value": f"₹ {product.grand_total:.2f}"
#                     }
#                 ],
#                 "stone_price_total": str(product.stone_price_total),
#                 "subtotal": str(product.subtotal),
#                 "grand_total": str(product.grand_total),
#                 "stones": [s.name for s in product.stones.all()],
#                 "average_rating": product.average_rating,
#                 "available_stock": product.available_stock,
#                 "stock_message": "Out of stock" if product.available_stock == 0 else "In stock",
#                 "is_wishlisted": False,
#                 "category": product.category.name,
#                 "occasion": product.occasion.name,
#                 "gender": product.gender.name,
#                 "metal": product.metal.name,
#                 "brand": "My Jewellery",
#                 "details": [
#                     {
#                         "title": "Metal Details",
#                         "content": [
#                             {"heading": f"{product.karat}K", "discription": "Karatage"},
#                             {"heading": "Yellow", "discription": "Material Colour"},
#                             {"heading": f"{product.metal_weight}g", "discription": "Gross Weight"},
#                             {"heading": product.metal.name, "discription": "Metal"},
#                         ],
#                     },
#                     {
#                         "title": "General Details",
#                         "content": [
#                             {"heading": "Jewelry", "discription": "Jewellery Type"},
#                             {"heading": "My Jewellery", "discription": "Brand"},
#                             {"heading": "Best Sellers", "discription": "Collection"},
#                             {"heading": product.gender.name, "discription": "Gender"},
#                             {"heading": product.occasion.name, "discription": "Occasion"},
#                         ],
#                     },
#                     {
#                         "title": "Description",
#                         "content": [
#                             {"description": product.description or ""}
#                         ]
#                     }
#                 ],
#                 "head": product.head,
#                 "size": product.size,
#                 "metal_weight": str(product.metal_weight),
#                 "karat": product.karat,
#                 "images": product.images if product.images else [],
#                 "ar_model_glb": product.ar_model_glb,
#                 "ar_model_gltf": product.ar_model_gltf,
#                 "description": product.description,
#                 "pendant_width": product.pendant_width,
#                 "pendant_height": product.pendant_height,
#                 "frozen_unit_price": str(product.frozen_unit_price),
#                 "making_charge": str(product.making_charge),
#                 "making_discount": str(product.making_discount),
#                 "product_discount": str(product.product_discount),
#                 "gst": str(product.gst),
#                 "handcrafted_charge": str(product.handcrafted_charge),
#                 "is_handcrafted": product.is_handcrafted,
#                 "is_classic": product.is_classic,
#                 "designing_charge": str(product.designing_charge),
#                 "total_stock": product.total_stock,
#                 "sold_count": product.sold_count,
#                 "created_at": product.created_at,
#                 "Subcategories": product.Subcategories.id if product.Subcategories else None,
#             })

#         # Final filters data with dynamic price range inside
#         filters = {
#             "category": list(Category.objects.values("id", "name")),
#             "metal": list(Metal.objects.values_list("name", flat=True)),
#             "gemstone": list(Gemstone.objects.values_list("name", flat=True)),
#             "brand": "My Jewellery My Design",
#             "colors": [
#                 {
#                     "color": "Yellow",
#                     "code": "#ffff00"
#                 }
#             ],
#             "price_range": {
#                 "min": min(prices) if prices else None,
#                 "max": max(prices) if prices else None
#             }
#         }

#         return Response({
#             "products": filtered_products,
#             "filters": filters
#         }, status=status.HTTP_200_OK)

# class PriceRangeProductAPIView(APIView):
#     """
#     POST: /api/products/by-price-range/
#     Accepts form-data: range_id, category (multi), metal (multi), gemstone (multi), brand, colors, min_price, max_price
#     Returns filtered products and updated filters.
#     """

#     def get_price_range(self, range_id):
#         price_map = {
#             1: (0, 25000),
#             2: (25000, 50000),
#             3: (50000, 100000),
#             4: (100000, None),  # 1L & above
#         }
#         return price_map.get(range_id, (None, None))

#     def post(self, request):
#         try:
#             range_id = int(request.data.get("range_id"))
#         except (TypeError, ValueError):
#             return Response({"detail": "Invalid or missing range_id"}, status=400)

#         range_min, range_max = self.get_price_range(range_id)
#         if range_min is None:
#             return Response({"detail": "Invalid range_id"}, status=400)

#         # Form-data filters
#         category_ids = request.data.getlist("category")
#         metals = request.data.getlist("metal")
#         gemstones = request.data.getlist("gemstone")
#         brand = request.data.get("brand")
#         color_codes = request.data.getlist("colors")
#         user_min_price = request.data.get("min_price")
#         user_max_price = request.data.get("max_price")

#         products = Product.objects.all()

#         if category_ids:
#             products = products.filter(category__id__in=category_ids)

#         if metals:
#             products = products.filter(metal__name__in=metals)

#         if gemstones:
#             products = products.filter(stones__name__in=gemstones).distinct()

#         if brand:
#             products = products.filter(brand__iexact=brand)

#         if color_codes:
#             color_filter = Q()
#             for code in color_codes:
#                 color_filter |= Q(colors__icontains=code)
#             products = products.filter(color_filter)

#         # Apply price range filter
#         if user_min_price and user_max_price:
#             try:
#                 min_price = max(float(user_min_price), range_min)
#                 max_price = min(float(user_max_price), range_max or float('inf'))
#             except ValueError:
#                 min_price = range_min
#                 max_price = range_max or float('inf')
#         else:
#             min_price = range_min
#             max_price = range_max or float('inf')

#         filtered_products = []
#         prices = []

#         for product in products:
#             price = float(product.grand_total or 0)
#             if price < min_price or price >= max_price:
#                 continue

#             prices.append(price)
#             filtered_products.append({
#                 "id": product.id,
#                 "unit_price": str(product.frozen_unit_price or product.metal.unit_price),
#                 "value": str((product.metal_weight * (product.frozen_unit_price or product.metal.unit_price)).quantize(Decimal('0.001'))),
#                 "items": [
#                     {
#                         "type": "product",
#                         "name": product.metal.name,
#                         "subLabel": f"{product.karat}KT" if product.karat else "",
#                         "rate": f"₹ {(product.frozen_unit_price or product.metal.unit_price):.2f}/g",
#                         "weight": f"{product.metal_weight}g",
#                         "discount": "_",
#                         "value": f"₹ {(product.metal_weight * (product.frozen_unit_price or product.metal.unit_price)).quantize(Decimal('0.01'))}",
#                         "image": product.images[0] if product.images else ""
#                     },
#                     {
#                         "type": "charges",
#                         "label": "Making Charges",
#                         "rate": "_",
#                         "weight": "_",
#                         "discount": "-",
#                         "value": f"₹ {product.making_charge:.2f}"
#                     },
#                     {
#                         "type": "subtotal",
#                         "label": "Sub Total",
#                         "rate": "_",
#                         "weight": f"{product.metal_weight}g Gross Wt.",
#                         "discount": "-",
#                         "value": f"₹ {product.subtotal:.2f}"
#                     },
#                     {
#                         "type": "gst",
#                         "label": "GST",
#                         "rate": "",
#                         "weight": "_",
#                         "discount": "-",
#                         "value": f"₹ {(product.subtotal * (product.gst / 100)).quantize(Decimal('0.01'))}"
#                     },
#                     {
#                         "type": "charges",
#                         "label": "Grand Total",
#                         "rate": "_",
#                         "weight": "_",
#                         "discount": "-",
#                         "value": f"₹ {product.grand_total:.2f}"
#                     }
#                 ],
#                 "stone_price_total": str(product.stone_price_total),
#                 "subtotal": str(product.subtotal),
#                 "grand_total": str(product.grand_total),
#                 "stones": [s.name for s in product.stones.all()],
#                 "average_rating": product.average_rating,
#                 "available_stock": product.available_stock,
#                 "stock_message": "Out of stock" if product.available_stock == 0 else "In stock",
#                 "is_wishlisted": False,
#                 "category": product.category.name,
#                 "occasion": product.occasion.name,
#                 "gender": product.gender.name,
#                 "metal": product.metal.name,
#                 "brand": "My Jewellery",
#                 "details": [
#                     {
#                         "title": "Metal Details",
#                         "content": [
#                             {"heading": f"{product.karat}K", "discription": "Karatage"},
#                             {"heading": "Yellow", "discription": "Material Colour"},
#                             {"heading": f"{product.metal_weight}g", "discription": "Gross Weight"},
#                             {"heading": product.metal.name, "discription": "Metal"},
#                         ],
#                     },
#                     {
#                         "title": "General Details",
#                         "content": [
#                             {"heading": "Jewelry", "discription": "Jewellery Type"},
#                             {"heading": "My Jewellery", "discription": "Brand"},
#                             {"heading": "Best Sellers", "discription": "Collection"},
#                             {"heading": product.gender.name, "discription": "Gender"},
#                             {"heading": product.occasion.name, "discription": "Occasion"},
#                         ],
#                     },
#                     {
#                         "title": "Description",
#                         "content": [
#                             {"description": product.description or ""}
#                         ]
#                     }
#                 ],
#                 "head": product.head,
#                 "size": product.size,
#                 "metal_weight": str(product.metal_weight),
#                 "karat": product.karat,
#                 "images": product.images if product.images else [],
#                 "ar_model_glb": product.ar_model_glb,
#                 "ar_model_gltf": product.ar_model_gltf,
#                 "description": product.description,
#                 "pendant_width": product.pendant_width,
#                 "pendant_height": product.pendant_height,
#                 "frozen_unit_price": str(product.frozen_unit_price),
#                 "making_charge": str(product.making_charge),
#                 "making_discount": str(product.making_discount),
#                 "product_discount": str(product.product_discount),
#                 "gst": str(product.gst),
#                 "handcrafted_charge": str(product.handcrafted_charge),
#                 "is_handcrafted": product.is_handcrafted,
#                 "is_classic": product.is_classic,
#                 "designing_charge": str(product.designing_charge),
#                 "total_stock": product.total_stock,
#                 "sold_count": product.sold_count,
#                 "created_at": product.created_at,
#                 "Subcategories": product.Subcategories.id if product.Subcategories else None,
#             })

#         filters = {
#             "category": list(Category.objects.values("id", "name")),
#             "metal": list(Metal.objects.values_list("name", flat=True)),
#             "gemstone": list(Gemstone.objects.values_list("name", flat=True)),
#             "brand": "My Jewellery My Design",
#             "colors": [{"color": "Yellow", "code": "#ffff00"}],
#             "price_range": {
#                 "min": min(prices) if prices else None,
#                 "max": max(prices) if prices else None
#             }
#         }

#         return Response({
#             "products": filtered_products,
#             "filters": filters
#         }, status=status.HTTP_200_OK)


# class PriceRangeProductAPIView(APIView):
#     """
#     POST or GET: /api/products/by-price-range/
#     Accepts form-data or query params: range_id, category (multi), metal (multi), gemstone (multi), brand, colors, min_price, max_price
#     Returns filtered products and updated filters.
#     """

#     def get_price_range(self, range_id):
#         price_map = {
#             1: (0, 25000),
#             2: (25000, 50000),
#             3: (50000, 100000),
#             4: (100000, None),  # 1L & above
#         }
#         return price_map.get(range_id, (None, None))

#     def get(self, request):
#         return self.filter_products(request.query_params)

#     def post(self, request):
#         return self.filter_products(request.data)

#     def filter_products(self, data):
#         try:
#             range_id = int(data.get("range_id", 0))
#         except (TypeError, ValueError):
#             return Response({"detail": "Invalid or missing range_id"}, status=400)

#         range_min, range_max = self.get_price_range(range_id)
#         if range_min is None:
#             return Response({"detail": "Invalid range_id"}, status=400)

#         # Filters
#         category_ids = data.getlist("category")
#         metals = data.getlist("metal")
#         gemstones = data.getlist("gemstone")
#         brand = data.get("brand")
#         color_codes = data.getlist("colors")
#         user_min_price = data.get("min_price")
#         user_max_price = data.get("max_price")

#         products = Product.objects.all()

#         if category_ids:
#             products = products.filter(category__id__in=category_ids)

#         if metals:
#             products = products.filter(metal__name__in=metals)

#         if gemstones:
#             products = products.filter(stones__name__in=gemstones).distinct()

#         if brand:
#             products = products.filter(brand__iexact=brand)

#         if color_codes:
#             color_filter = Q()
#             for code in color_codes:
#                 color_filter |= Q(colors__icontains=code)
#             products = products.filter(color_filter)

#         # Price filtering
#         try:
#             min_price = max(float(user_min_price), range_min) if user_min_price else range_min
#             max_price = min(float(user_max_price), range_max or float('inf')) if user_max_price else (range_max or float('inf'))
#         except ValueError:
#             min_price = range_min
#             max_price = range_max or float('inf')

#         filtered_products = []
#         prices = []

#         for product in products:
#             price = float(product.grand_total or 0)
#             if price < min_price or price >= max_price:
#                 continue

#             prices.append(price)
#             filtered_products.append({
#                 "id": product.id,
#                 "name": str(product),
#                 "grand_total": str(product.grand_total),
#                 "metal": product.metal.name,
#                 "category": product.category.name,
#                 # Add other required fields...
#             })

#         filters = {
#             "category": list(Category.objects.values("id", "name")),
#             "metal": list(Metal.objects.values_list("name", flat=True)),
#             "gemstone": list(Gemstone.objects.values_list("name", flat=True)),
#             "brand": "My Jewellery My Design",
#             "colors": [{"color": "Yellow", "code": "#ffff00"}],
#             "price_range": {
#                 "min": min(prices) if prices else None,
#                 "max": max(prices) if prices else None
#             }
#         }

#         return Response({
#             "products": filtered_products,
#             "filters": filters
#         }, status=status.HTTP_200_OK)


# class PriceRangeProductAPIView(APIView):
#     """
#     GET or POST: /api/products/by-price-range/
#     Filters:
#         - range_id (required)
#         - category (multiple)
#         - metal (multiple)
#         - gemstone (multiple)
#         - brand
#         - colors (multiple)
#         - min_price (optional)
#         - max_price (optional)
#     """

#     def get_price_range(self, range_id):
#         price_map = {
#             1: (0, 25000),
#             2: (25000, 50000),
#             3: (50000, 100000),
#             4: (100000, None),  # 1L & above
#         }
#         return price_map.get(range_id, (None, None))

#     def get(self, request):
#         return self.filter_products(request)

#     def post(self, request):
#         return self.filter_products(request)

#     def filter_products(self, request):
#         data = request.data
#         query = request.query_params

#         try:
#             range_id = int(data.get("range_id") or query.get("range_id", 0))
#         except (TypeError, ValueError):
#             return Response({"detail": "Invalid or missing range_id"}, status=400)

#         range_min, range_max = self.get_price_range(range_id)
#         if range_min is None:
#             return Response({"detail": f"Invalid range_id: {range_id}"}, status=400)

#         get_list = data.getlist if hasattr(data, "getlist") else lambda key: data.get(key, [])
#         category_names = get_list("category") or query.getlist("category")
#         metals = get_list("metal") or query.getlist("metal")
#         gemstones = get_list("gemstone") or query.getlist("gemstone")
#         brand = data.get("brand") or query.get("brand")
#         color_codes = get_list("colors") or query.getlist("colors")
#         user_min_price = data.get("min_price") or query.get("min_price")
#         user_max_price = data.get("max_price") or query.get("max_price")

#         products = Product.objects.all()

#         # ✅ Use name instead of id
#         if category_names:
#             products = products.filter(category__name__in=category_names)

#         if metals:
#             products = products.filter(metal__name__in=metals)

#         if gemstones:
#             products = products.filter(stones__name__in=gemstones).distinct()

#         if brand:
#             products = products.filter(brand__iexact=brand)

#         if color_codes:
#             color_filter = Q()
#             for code in color_codes:
#                 color_filter |= Q(colors__icontains=code)
#             products = products.filter(color_filter)

#         try:
#             min_price = max(float(user_min_price), range_min) if user_min_price else range_min
#             max_price = min(float(user_max_price), range_max or float('inf')) if user_max_price else (range_max or float('inf'))
#         except ValueError:
#             min_price = range_min
#             max_price = range_max or float('inf')

#         filtered_products = []
#         prices = []

#         for product in products:
#             price = float(product.grand_total or 0)
#             if price < min_price or price >= max_price:
#                 continue

#             prices.append(price)
#             filtered_products.append({
#                 "id": product.id,
#                 "name": str(product),
#                 "grand_total": str(product.grand_total),
#                 "metal": product.metal.name,
#                 "category": product.category.name,
#             })

#         filters = {
#             "category": list(Category.objects.values("id", "name")),
#             "metal": list(Metal.objects.values_list("name", flat=True)),
#             "gemstone": list(Gemstone.objects.values_list("name", flat=True)),
#             "brand": "My Jewellery My Design",
#             "colors": [{"color": "Yellow", "code": "#ffff00"}],
#             "price_range": {
#                 "min": min(prices) if prices else None,
#                 "max": max(prices) if prices else None
#             }
#         }

#         return Response({
#             "products": filtered_products,
#             "filters": filters
#         }, status=status.HTTP_200_OK)


# class PriceRangeProductAPIView(APIView):
#     """
#     GET: /api/products/by-price-range/?range_id=3
#         - Uses predefined price ranges via `range_id`.

#     POST: /api/products/by-price-range/
#         - Uses custom min_price and max_price.

#     Optional Filters (GET & POST):
#         - category (list of names)
#         - metal (list of names)
#         - gemstone (list of names)
#         - brand (string)
#         - colors (list of hex codes)
#     """

#     def get_price_range(self, range_id):
#         price_map = {
#             1: (0, 25000),
#             2: (25000, 50000),
#             3: (50000, 100000),
#             4: (100000, None),
#         }
#         return price_map.get(range_id, (None, None))

#     def get(self, request):
#         return self.filter_products(request, use_range_id=True)

#     def post(self, request):
#         return self.filter_products(request, use_range_id=False)

#     def filter_products(self, request, use_range_id=False):
#         data = request.data if request.method == "POST" else request.query_params

#         # --- Price Range Logic ---
#         if use_range_id:
#             try:
#                 range_id = int(data.get("range_id", 0))
#             except (ValueError, TypeError):
#                 return Response({"detail": "Invalid or missing range_id"}, status=400)

#             range_min, range_max = self.get_price_range(range_id)
#             if range_min is None:
#                 return Response({"detail": f"Invalid range_id: {range_id}"}, status=400)
#         else:
#             try:
#                 range_min = float(data.get("min_price", 0))
#                 range_max = float(data.get("max_price", float('inf')))
#             except (ValueError, TypeError):
#                 return Response({"detail": "Invalid price range"}, status=400)

#         # --- Get list filters ---
#         get_list = data.getlist if hasattr(data, "getlist") else lambda key: data.get(key, [])
#         category_names = get_list("category")
#         metals = get_list("metal")
#         gemstones = get_list("gemstone")
#         brand = data.get("brand")
#         color_codes = get_list("colors")

#         # --- Query products ---
#         products = Product.objects.all()

#         if category_names:
#             products = products.filter(category__name__in=category_names)

#         if metals:
#             products = products.filter(metal__name__in=metals)

#         if gemstones:
#             products = products.filter(stones__name__in=gemstones).distinct()

#         if brand:
#             products = products.filter(brand__iexact=brand)

#         if color_codes:
#             color_filter = Q()
#             for code in color_codes:
#                 color_filter |= Q(colors__icontains=code)
#             products = products.filter(color_filter)

#         # --- Filter by price range ---
#         filtered_products = []
#         prices = []

#         for product in products:
#             price = float(product.grand_total or 0)
#             if price < range_min or price > range_max:
#                 continue
#             prices.append(price)
#             filtered_products.append({
#                 "id": product.id,
#                 "name": str(product),
#                 "grand_total": str(product.grand_total),
#                 "metal": product.metal.name,
#                 "category": product.category.name,
#             })

#         filters = {
#             "category": list(Category.objects.values("id", "name")),
#             "metal": list(Metal.objects.values_list("name", flat=True)),
#             "gemstone": list(Gemstone.objects.values_list("name", flat=True)),
#             "brand": "My Jewellery My Design",
#             "colors": [{"color": "Yellow", "code": "#ffff00"}],
#             "price_range": {
#                 "min": min(prices) if prices else None,
#                 "max": max(prices) if prices else None,
#             }
#         }

#         return Response({
#             "products": filtered_products,
#             "filters": filters,
#         }, status=status.HTTP_200_OK)



# class PriceRangeProductAPIView(APIView):
#     """
#     GET: /api/products/by-price-range/?range_id=3
#         - Uses predefined price ranges via `range_id`.

#     POST: /api/products/by-price-range/
#         - Uses custom min_price and max_price.

#     Optional Filters (GET & POST):
#         - category (list of names)
#         - metal (list of names)
#         - gemstone (list of names)
#         - brand (string)
#         - colors (list of hex codes)
#     """

#     def get_price_range(self, range_id):
#         price_map = {
#             1: (0, 25000),
#             2: (25000, 50000),
#             3: (50000, 100000),
#             4: (100000, None),
#         }
#         return price_map.get(range_id, (None, None))

#     def get(self, request):
#         return self.filter_products(request, use_range_id=True)

#     def post(self, request):
#         return self.filter_products(request, use_range_id=False)

#     def filter_products(self, request, use_range_id=False):
#         data = request.data if request.method == "POST" else request.query_params

#         # --- Price Range Logic ---
#         if use_range_id:
#             try:
#                 range_id = int(data.get("range_id", 0))
#             except (ValueError, TypeError):
#                 return Response({"detail": "Invalid or missing range_id"}, status=400)

#             range_min, range_max = self.get_price_range(range_id)
#             if range_min is None:
#                 return Response({"detail": f"Invalid range_id: {range_id}"}, status=400)
#         else:
#             try:
#                 range_min = float(data.get("min_price", 0))
#                 range_max = float(data.get("max_price", float('inf')))
#             except (ValueError, TypeError):
#                 return Response({"detail": "Invalid price range"}, status=400)

#         # --- Helper to extract lists safely ---
#         get_list = data.getlist if hasattr(data, "getlist") else lambda k: data.get(k, []) if isinstance(data.get(k, []), list) else [data.get(k)] if data.get(k) else []

#         # --- Extract Filters ---
#         category_names = get_list("category")
#         metals = get_list("metal")
#         gemstones = get_list("gemstone")
#         brand = data.get("brand")
#         color_codes = get_list("colors")

#         # --- Query Products ---
#         products = Product.objects.all()

#         if category_names:
#             products = products.filter(category__name__in=category_names)

#         if metals:
#             products = products.filter(metal__name__in=metals)

#         if gemstones:
#             products = products.filter(stones__name__in=gemstones).distinct()

#         if brand:
#             products = products.filter(brand__iexact=brand)

#         if color_codes:
#             color_filter = Q()
#             for code in color_codes:
#                 color_filter |= Q(colors__icontains=code)
#             products = products.filter(color_filter)

#         # --- Price Range Filtering ---
#         filtered_products = []
#         prices = []

#         for product in products:
#             price = float(product.grand_total or 0)
#             if price < range_min or price > range_max:
#                 continue
#             prices.append(price)
#             filtered_products.append({
#                 "id": product.id,
#                 "name": str(product),
#                 "grand_total": str(product.grand_total),
#                 "metal": product.metal.name,
#                 "category": product.category.name,
#             })

#         # --- Return Filters (static or preloaded) ---
#         filters = {
#             "category": list(Category.objects.values("id", "name")),
#             "metal": list(Metal.objects.values_list("name", flat=True)),
#             "gemstone": list(Gemstone.objects.values_list("name", flat=True)),
#             "brand": "My Jewellery My Design",
#             "colors": [{"color": "Yellow", "code": "#ffff00"}],
#             "price_range": {
#                 "min": min(prices) if prices else None,
#                 "max": max(prices) if prices else None,
#             }
#         }

#         return Response({
#             "products": filtered_products,
#             "filters": filters,
#         }, status=status.HTTP_200_OK)

# class PriceRangeProductAPIView(APIView):
#     """
#     POST: /api/products/by-price-range/
#     Accepts form-data: range_id, category (multi), metal (multi), gemstone (multi), brand, colors, min_price, max_price
#     Returns filtered products and updated filters.
#     """

#     def get_price_range(self, range_id):
#         price_map = {
#             1: (0, 25000),
#             2: (25000, 50000),
#             3: (50000, 100000),
#             4: (100000, None),  # 1L & above
#         }
#         return price_map.get(range_id, (None, None))

#     def get(self, request):
#         return self.post(request)

#     def post(self, request):
#         try:
#             range_id = int(request.data.get("range_id"))
#         except (TypeError, ValueError):
#             return Response({"detail": "Invalid or missing range_id"}, status=400)

#         range_min, range_max = self.get_price_range(range_id)
#         if range_min is None:
#             return Response({"detail": "Invalid range_id"}, status=400)

#         # Form-data filters
#         category_ids = request.data.getlist("category")
#         metals = request.data.getlist("metal")
#         gemstones = request.data.getlist("gemstone")
#         brand = request.data.get("brand")
#         color_codes = request.data.getlist("colors")
#         user_min_price = request.data.get("min_price")
#         user_max_price = request.data.get("max_price")

#         products = Product.objects.all()

#         if category_ids:
#             products = products.filter(category__id__in=category_ids)

#         if metals:
#             products = products.filter(metal__name__in=metals)

#         if gemstones:
#             products = products.filter(stones__name__in=gemstones).distinct()

#         if brand:
#             products = products.filter(brand__iexact=brand)

#         if color_codes:
#             color_filter = Q()
#             for code in color_codes:
#                 color_filter |= Q(colors__icontains=code)
#             products = products.filter(color_filter)

#         # Apply price range filter
#         if user_min_price and user_max_price:
#             try:
#                 min_price = max(float(user_min_price), range_min)
#                 max_price = min(float(user_max_price), range_max or float('inf'))
#             except ValueError:
#                 min_price = range_min
#                 max_price = range_max or float('inf')
#         else:
#             min_price = range_min
#             max_price = range_max or float('inf')

#         filtered_products = []
#         prices = []

#         for product in products:
#             price = float(product.grand_total or 0)
#             if price < min_price or price >= max_price:
#                 continue

#             prices.append(price)
#             filtered_products.append({
#                 "id": product.id,
#                 "unit_price": str(product.frozen_unit_price or product.metal.unit_price),
#                 "value": str((product.metal_weight * (product.frozen_unit_price or product.metal.unit_price)).quantize(Decimal('0.001'))),
#                 "items": [
#                     {
#                         "type": "product",
#                         "name": product.metal.name,
#                         "subLabel": f"{product.karat}KT" if product.karat else "",
#                         "rate": f"₹ {(product.frozen_unit_price or product.metal.unit_price):.2f}/g",
#                         "weight": f"{product.metal_weight}g",
#                         "discount": "_",
#                         "value": f"₹ {(product.metal_weight * (product.frozen_unit_price or product.metal.unit_price)).quantize(Decimal('0.01'))}",
#                         "image": product.images[0] if product.images else ""
#                     },
#                     {
#                         "type": "charges",
#                         "label": "Making Charges",
#                         "rate": "_",
#                         "weight": "_",
#                         "discount": "-",
#                         "value": f"₹ {product.making_charge:.2f}"
#                     },
#                     {
#                         "type": "subtotal",
#                         "label": "Sub Total",
#                         "rate": "_",
#                         "weight": f"{product.metal_weight}g Gross Wt.",
#                         "discount": "-",
#                         "value": f"₹ {product.subtotal:.2f}"
#                     },
#                     {
#                         "type": "gst",
#                         "label": "GST",
#                         "rate": "",
#                         "weight": "_",
#                         "discount": "-",
#                         "value": f"₹ {(product.subtotal * (product.gst / 100)).quantize(Decimal('0.01'))}"
#                     },
#                     {
#                         "type": "charges",
#                         "label": "Grand Total",
#                         "rate": "_",
#                         "weight": "_",
#                         "discount": "-",
#                         "value": f"₹ {product.grand_total:.2f}"
#                     }
#                 ],
#                 "stone_price_total": str(product.stone_price_total),
#                 "subtotal": str(product.subtotal),
#                 "grand_total": str(product.grand_total),
#                 "stones": [s.name for s in product.stones.all()],
#                 "average_rating": product.average_rating,
#                 "available_stock": product.available_stock,
#                 "stock_message": "Out of stock" if product.available_stock == 0 else "In stock",
#                 "is_wishlisted": False,
#                 "category": product.category.name,
#                 "occasion": product.occasion.name,
#                 "gender": product.gender.name,
#                 "metal": product.metal.name,
#                 "brand": "My Jewellery",
#                 "details": [
#                     {
#                         "title": "Metal Details",
#                         "content": [
#                             {"heading": f"{product.karat}K", "discription": "Karatage"},
#                             {"heading": "Yellow", "discription": "Material Colour"},
#                             {"heading": f"{product.metal_weight}g", "discription": "Gross Weight"},
#                             {"heading": product.metal.name, "discription": "Metal"},
#                         ],
#                     },
#                     {
#                         "title": "General Details",
#                         "content": [
#                             {"heading": "Jewelry", "discription": "Jewellery Type"},
#                             {"heading": "My Jewellery", "discription": "Brand"},
#                             {"heading": "Best Sellers", "discription": "Collection"},
#                             {"heading": product.gender.name, "discription": "Gender"},
#                             {"heading": product.occasion.name, "discription": "Occasion"},
#                         ],
#                     },
#                     {
#                         "title": "Description",
#                         "content": [
#                             {"description": product.description or ""}
#                         ]
#                     }
#                 ],
#                 "head": product.head,
#                 "size": product.size,
#                 "metal_weight": str(product.metal_weight),
#                 "karat": product.karat,
#                 "images": product.images if product.images else [],
#                 "ar_model_glb": product.ar_model_glb,
#                 "ar_model_gltf": product.ar_model_gltf,
#                 "description": product.description,
#                 "pendant_width": product.pendant_width,
#                 "pendant_height": product.pendant_height,
#                 "frozen_unit_price": str(product.frozen_unit_price),
#                 "making_charge": str(product.making_charge),
#                 "making_discount": str(product.making_discount),
#                 "product_discount": str(product.product_discount),
#                 "gst": str(product.gst),
#                 "handcrafted_charge": str(product.handcrafted_charge),
#                 "is_handcrafted": product.is_handcrafted,
#                 "is_classic": product.is_classic,
#                 "designing_charge": str(product.designing_charge),
#                 "total_stock": product.total_stock,
#                 "sold_count": product.sold_count,
#                 "created_at": product.created_at,
#                 "Subcategories": product.Subcategories.id if product.Subcategories else None,
#             })

#         filters = {
#             "category": list(Category.objects.values("id", "name")),
#             "metal": list(Metal.objects.values_list("name", flat=True)),
#             "gemstone": list(Gemstone.objects.values_list("name", flat=True)),
#             "brand": "My Jewellery My Design",
#             "colors": [{"color": "Yellow", "code": "#ffff00"}],
#             "price_range": {
#                 "min": min(prices) if prices else None,
#                 "max": max(prices) if prices else None
#             }
#         }

#         return Response({
#             "products": filtered_products,
#             "filters": filters
#         }, status=status.HTTP_200_OK)


# class PriceRangeProductAPIView(APIView):
#     """
#     GET: /api/products/by-price-range/?range_id=3
#         - Uses predefined price ranges via `range_id`.

#     POST: /api/products/by-price-range/
#         - Uses custom min_price and max_price.
#         - If not provided, uses fallback `range_id`.

#     Optional Filters (GET & POST):
#         - category (list of names)
#         - metal (list of names)
#         - gemstone (list of names)
#         - brand (string)
#         - colors (list of hex codes)
#     """

#     def get_price_range(self, range_id):
#         price_map = {
#             1: (0, 25000),
#             2: (25000, 50000),
#             3: (50000, 100000),
#             4: (100000, None),
#         }
#         return price_map.get(range_id, (None, None))

#     def get(self, request):
#         return self.filter_products(request, use_range_id=True)

#     def post(self, request):
#         return self.filter_products(request, use_range_id=False)

#     def filter_products(self, request, use_range_id=False):
#         data = request.data if request.method == "POST" else request.query_params

#         # --- Price Range Logic ---
#         if use_range_id:
#             try:
#                 range_id = int(data.get("range_id", 0))
#             except (ValueError, TypeError):
#                 return Response({"detail": "Invalid or missing range_id"}, status=400)

#             range_min, range_max = self.get_price_range(range_id)
#             if range_min is None:
#                 return Response({"detail": f"Invalid range_id: {range_id}"}, status=400)

#         else:
#             try:
#                 min_price_raw = data.get("min_price")
#                 max_price_raw = data.get("max_price")

#                 if min_price_raw is not None and max_price_raw is not None:
#                     range_min = float(min_price_raw)
#                     range_max = float(max_price_raw)
#                 else:
#                     # Fallback to range_id logic
#                     range_id = int(data.get("range_id", 0))
#                     range_min, range_max = self.get_price_range(range_id)

#                     if range_min is None:
#                         return Response({"detail": "Price range missing and fallback range_id is invalid or missing."}, status=400)
#             except (ValueError, TypeError):
#                 return Response({"detail": "Invalid price values. Must be numeric."}, status=400)

#         # --- Helper to extract lists safely ---
#         get_list = data.getlist if hasattr(data, "getlist") else lambda k: data.get(k, []) if isinstance(data.get(k, []), list) else [data.get(k)] if data.get(k) else []

#         # --- Extract Filters ---
#         category_names = get_list("category")
#         metals = get_list("metal")
#         gemstones = get_list("gemstone")
#         brand = data.get("brand")
#         color_codes = get_list("colors")

#         # --- Query Products ---
#         products = Product.objects.all()

#         if category_names:
#             products = products.filter(category__name__in=category_names)

#         if metals:
#             products = products.filter(metal__name__in=metals)

#         if gemstones:
#             products = products.filter(stones__name__in=gemstones).distinct()

#         if brand:
#             products = products.filter(brand__iexact=brand)

#         if color_codes:
#             color_filter = Q()
#             for code in color_codes:
#                 color_filter |= Q(colors__icontains=code)
#             products = products.filter(color_filter)

#         # --- Price Range Filtering ---
#         filtered_products = []
#         prices = []

#         for product in products:
#             price = float(product.grand_total or 0)
#             if range_max is not None and (price < range_min or price > range_max):
#                 continue
#             elif range_max is None and price < range_min:
#                 continue

#             prices.append(price)
#             filtered_products.append({
#                 "id": product.id,
#                 "name": str(product),
#                 "grand_total": str(product.grand_total),
#                 "metal": product.metal.name,
#                 "category": product.category.name,
#             })

#         # --- Return Filters (static or preloaded) ---
#         filters = {
#             "category": list(Category.objects.values("id", "name")),
#             "metal": list(Metal.objects.values_list("name", flat=True)),
#             "gemstone": list(Gemstone.objects.values_list("name", flat=True)),
#             "brand": "My Jewellery My Design",
#             "colors": [{"color": "Yellow", "code": "#ffff00"}],
#             "price_range": {
#                 "min": min(prices) if prices else None,
#                 "max": max(prices) if prices else None,
#             }
#         }

#         return Response({
#             "products": filtered_products,
#             "filters": filters,
#         }, status=status.HTTP_200_OK)



# important

# class PriceRangeProductAPIView(APIView):
#     """
#     GET: /api/products/by-price-range/?range_id=3
#         - Uses predefined price ranges via `range_id`.

#     POST: /api/products/by-price-range/?range_id=3
#         - Uses custom min_price and max_price if provided.
#         - If not, falls back to `range_id` from query params.

#     Optional Filters (GET & POST):
#         - category (list of names)
#         - metal (list of names)
#         - gemstone (list of names)
#         - brand (string)
#         - colors (list of hex codes)
#     """

#     def get_price_range(self, range_id):
#         price_map = {
#             1: (0, 25000),
#             2: (25000, 50000),
#             3: (50000, 100000),
#             4: (100000, None),
#         }
#         return price_map.get(range_id, (None, None))

#     def get(self, request):
#         return self.filter_products(request, use_range_id=True)

#     def post(self, request):
#         return self.filter_products(request, use_range_id=False)

#     def filter_products(self, request, use_range_id=False):
#         data = request.data if request.method == "POST" else request.query_params

#         # --- Price Range Logic ---
#         if use_range_id:
#             try:
#                 range_id = int(request.query_params.get("range_id", 0))
#                 range_min, range_max = self.get_price_range(range_id)
#                 if range_min is None:
#                     return Response({"detail": f"Invalid range_id: {range_id}"}, status=400)
#             except (ValueError, TypeError):
#                 return Response({"detail": "Invalid or missing range_id"}, status=400)

#         else:
#             try:
#                 min_price_raw = data.get("min_price")
#                 max_price_raw = data.get("max_price")

#                 if min_price_raw is not None and max_price_raw is not None:
#                     range_min = float(min_price_raw)
#                     range_max = float(max_price_raw)
#                 else:
#                     # Fallback: get range_id from query_params
#                     try:
#                         range_id = int(request.query_params.get("range_id", 0))
#                     except (ValueError, TypeError):
#                         range_id = 0

#                     range_min, range_max = self.get_price_range(range_id)

#                     # Default to full range if range_id is invalid
#                     if range_min is None:
#                         range_min, range_max = 0, float("inf")

#             except (ValueError, TypeError):
#                 return Response({"detail": "Invalid price values. Must be numeric."}, status=400)

#         # --- Helper to extract lists safely ---
#         get_list = data.getlist if hasattr(data, "getlist") else lambda k: data.get(k, []) if isinstance(data.get(k, []), list) else [data.get(k)] if data.get(k) else []

#         # --- Extract Filters ---
#         category_names = get_list("category")
#         metals = get_list("metal")
#         gemstones = get_list("gemstone")
#         brand = data.get("brand")
#         color_codes = get_list("colors")

#         # --- Query Products ---
#         products = Product.objects.all()

#         if category_names:
#             products = products.filter(category__name__in=category_names)

#         if metals:
#             products = products.filter(metal__name__in=metals)

#         if gemstones:
#             products = products.filter(stones__name__in=gemstones).distinct()

#         if brand:
#             products = products.filter(brand__iexact=brand)

#         if color_codes:
#             color_filter = Q()
#             for code in color_codes:
#                 color_filter |= Q(colors__icontains=code)
#             products = products.filter(color_filter)

#         # --- Price Range Filtering ---
#         filtered_products = []
#         prices = []

#         for product in products:
#             price = float(product.grand_total or 0)
#             if range_max is not None and (price < range_min or price > range_max):
#                 continue
#             elif range_max is None and price < range_min:
#                 continue

#             prices.append(price)
#             filtered_products.append({
#                 "id": product.id,
#                 "name": str(product),
#                 "grand_total": str(product.grand_total),
#                 "metal": product.metal.name,
#                 "category": product.category.name,
#             })

#         # --- Return Filters (static or preloaded) ---
#         filters = {
#             "category": list(Category.objects.values("id", "name")),
#             "metal": list(Metal.objects.values_list("name", flat=True)),
#             "gemstone": list(Gemstone.objects.values_list("name", flat=True)),
#             "brand": "My Jewellery My Design",
#             "colors": [{"color": "Yellow", "code": "#ffff00"}],
#             "price_range": {
#                 "min": min(prices) if prices else None,
#                 "max": max(prices) if prices else None,
#             }
#         }

#         return Response({
#             "products": filtered_products,
#             "filters": filters,
#         }, status=status.HTTP_200_OK)


# class PriceRangeProductAPIView(APIView):
#     """
#     GET: /api/products/by-price-range/?range_id=3
#     POST: /api/products/by-price-range/?range_id=3
#         Accepts optional 'price': {"min_price": ..., "max_price": ...}
#     """

#     def get_price_range(self, range_id):
#         price_map = {
#             1: (0, 25000),
#             2: (25000, 50000),
#             3: (50000, 100000),
#             4: (100000, None),
#         }
#         return price_map.get(range_id, (None, None))

#     def get(self, request):
#         return self.filter_products(request, use_range_id=True)

#     def post(self, request):
#         return self.filter_products(request, use_range_id=False)

#     def filter_products(self, request, use_range_id=False):
#         data = request.data if request.method == "POST" else request.query_params

#         # --- Price Range Logic ---
#         if use_range_id:
#             try:
#                 range_id = int(request.query_params.get("range_id", 0))
#                 range_min, range_max = self.get_price_range(range_id)
#                 if range_min is None:
#                     return Response({"detail": f"Invalid range_id: {range_id}"}, status=400)
#             except (ValueError, TypeError):
#                 return Response({"detail": "Invalid or missing range_id"}, status=400)

#         else:
#             price_data = data.get("price", {})

#             # If form-data: parse JSON string manually
#             if isinstance(price_data, str):
#                 try:
#                     price_data = json.loads(price_data)
#                 except json.JSONDecodeError:
#                     price_data = {}

#             min_price_raw = price_data.get("min_price")
#             max_price_raw = price_data.get("max_price")

#             if min_price_raw is not None and max_price_raw is not None:
#                 try:
#                     range_min = float(min_price_raw)
#                     range_max = float(max_price_raw)
#                 except (ValueError, TypeError):
#                     return Response({"detail": "Invalid price values. Must be numeric."}, status=400)
#             else:
#                 # fallback to range_id from query
#                 try:
#                     range_id = int(request.query_params.get("range_id", 0))
#                 except (ValueError, TypeError):
#                     range_id = 0

#                 range_min, range_max = self.get_price_range(range_id)
#                 if range_min is None:
#                     range_min, range_max = 0, float("inf")

#         # --- Helper to extract lists safely ---
#         get_list = data.getlist if hasattr(data, "getlist") else lambda k: data.get(k, []) if isinstance(data.get(k, []), list) else [data.get(k)] if data.get(k) else []

#         # --- Extract Filters ---
#         category_names = get_list("category")
#         metals = get_list("metal")
#         gemstones = get_list("gemstone")
#         brand = data.get("brand")
#         color_codes = get_list("colors")

#         # --- Query Products ---
#         products = Product.objects.all()

#         if category_names:
#             products = products.filter(category__name__in=category_names)

#         if metals:
#             products = products.filter(metal__name__in=metals)

#         if gemstones:
#             products = products.filter(stones__name__in=gemstones).distinct()

#         if brand:
#             products = products.filter(brand__iexact=brand)

#         if color_codes:
#             color_filter = Q()
#             for code in color_codes:
#                 color_filter |= Q(colors__icontains=code)
#             products = products.filter(color_filter)

#         # --- Price Range Filtering ---
#         filtered_products = []
#         prices = []

#         for product in products:
#             price = float(product.grand_total or 0)
#             if range_max is not None and (price < range_min or price > range_max):
#                 continue
#             elif range_max is None and price < range_min:
#                 continue

#             prices.append(price)
#             filtered_products.append({
#                 "id": product.id,
#                 "name": str(product),
#                 "grand_total": str(product.grand_total),
#                 "metal": product.metal.name,
#                 "category": product.category.name,
#             })

#         # --- Return Filters ---
#         filter_category = {
#             "category": list(Category.objects.values("id", "name")),
#             "metal": list(Metal.objects.values_list("name", flat=True)),
#             "gemstone": list(Gemstone.objects.values_list("name", flat=True)),
#             "brand": "My Jewellery My Design",
#             "colors": [{"color": "Yellow", "code": "#ffff00"}],
#             "price_range": {
#                 "min": min(prices) if prices else None,
#                 "max": max(prices) if prices else None,
#             }
#         }

#         return Response({
#             "products": filtered_products,
#             "filter_category": filter_category,
#         }, status=status.HTTP_200_OK)

class PriceRangeProductAPIView(APIView):
    """
    GET: /api/products/by-price-range/?range_id=3
    POST: /api/products/by-price-range/?range_id=3
           Accepts optional 'price': {"min_price": ..., "max_price": ...}
    """

    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_price_range(self, range_id):
        price_map = {
            1: (0, 25000),
            2: (25000, 50000),
            3: (50000, 100000),
            4: (100000, None),
        }
        return price_map.get(range_id, (None, None))

    def get_price_label(self, range_id):
        label_map = {
            1: "<25K",
            2: "25K - 50K",
            3: "50K - 1L",
            4: "1L & Above",
        }
        return label_map.get(range_id, "Price Range")

    def get(self, request):
        return self.filter_products(request, use_range_id=True)

    def post(self, request):
        return self.filter_products(request, use_range_id=False)

    def filter_products(self, request, use_range_id=False):
        data = request.data if request.method == "POST" else request.query_params

        range_id = 0
        price_min = price_max = None

        if use_range_id:
            try:
                range_id = int(request.query_params.get("range_id", 0))
                price_min, price_max = self.get_price_range(range_id)
                if price_min is None:
                    return Response({"detail": f"Invalid range_id: {range_id}"}, status=400)
            except (ValueError, TypeError):
                return Response({"detail": "Invalid or missing range_id"}, status=400)
        else:
            price_data = data.get("price", {})
            if isinstance(price_data, str):
                try:
                    price_data = json.loads(price_data)
                except json.JSONDecodeError:
                    price_data = {}

            min_price_raw = price_data.get("min_price")
            max_price_raw = price_data.get("max_price")

            if min_price_raw is not None and max_price_raw is not None:
                try:
                    price_min = float(min_price_raw)
                    price_max = float(max_price_raw)
                except (ValueError, TypeError):
                    return Response({"detail": "Invalid price values. Must be numeric."}, status=400)
            else:
                try:
                    range_id = int(request.query_params.get("range_id", 0))
                except (ValueError, TypeError):
                    range_id = 0
                price_min, price_max = self.get_price_range(range_id)
                if price_min is None:
                    price_min, price_max = 0, float("inf")

        get_list = data.getlist if hasattr(data, "getlist") else lambda k: (
            data.get(k, []) if isinstance(data.get(k, []), list)
            else [data.get(k)] if data.get(k) else []
        )

        category_names = get_list("category")
        metals = get_list("metal")
        gemstones = get_list("gemstone")
        brand = data.get("brand")
        color_codes = get_list("colors")

        products = Product.objects.all()

        if category_names:
            products = products.filter(category__name__in=category_names)
        if metals:
            products = products.filter(metal__name__in=metals)
        if gemstones:
            products = products.filter(stones__name__in=gemstones).distinct()
        if brand:
            products = products.filter(brand__iexact=brand)
        if color_codes:
            color_filter = Q()
            for code in color_codes:
                color_filter |= Q(colors__icontains=code)
            products = products.filter(color_filter)

        # Use only IDs of filtered products for wishlist check
        product_ids = list(products.values_list("id", flat=True))
        user = request.user if request.user.is_authenticated else None
        wishlisted_ids = set()
        if user and product_ids:
            wishlisted_ids = set(
                Wishlist.objects.filter(user=user, product_id__in=product_ids)
                .values_list("product_id", flat=True)
            )

        filtered_products = []
        prices = []

        for product in products:
            price = float(product.grand_total or 0)
            if price_max is not None and (price < price_min or price > price_max):
                continue
            elif price_max is None and price < price_min:
                continue

            prices.append(price)
            filtered_products.append({
                "id": product.id,
                "head": product.head,
                "description": product.description,
                "first_image": product.images[0] if product.images else None,
                "average_rating": product.average_rating,
                "grand_total": str(product.grand_total),
                "is_wishlisted": product.id in wishlisted_ids
            })

        filter_category = [{
            "category": list(Category.objects.values("id", "name")),
            "metal": list(Metal.objects.values_list("name", flat=True)),
            "gemstone": list(Gemstone.objects.values_list("name", flat=True)),
            "brand": "My Jewellery My Design",
            "colors": [{"color": "Yellow", "code": "#ffff00"}],
            "price_range": {
                "min": min(prices) if prices else None,
                "max": max(prices) if prices else None,
            }
            }]

        category_label = self.get_price_label(range_id)

        return Response({
            "category": category_label,
            "products": filtered_products,
            "filter_category": filter_category,
        }, status=status.HTTP_200_OK)

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
    


# class ProductSearchAPIView(ListAPIView):
#     serializer_class = ProductSerializer

#     def get_queryset(self):
#         query = self.request.query_params.get('q', None)
#         is_handcrafted = self.request.query_params.get('is_handcrafted', None)

#         if query:
#             queryset = Product.objects.filter(
#                 Q(head__icontains=query) |
#                 Q(description__icontains=query) |
#                 Q(category__name__icontains=query) |
#                 Q(metal__name__icontains=query) |
#                 Q(metal__material__name__icontains=query) |
#                 Q(gender__name__icontains=query) |
#                 Q(occasion__name__icontains=query) |  # fixed field name here
#                 Q(stones__name__icontains=query)
#             ).distinct()
#         else:
#             queryset = Product.objects.all()

#         # Apply handcrafted filter if provided
#         if is_handcrafted is not None:
#             if is_handcrafted.lower() == 'true':
#                 queryset = queryset.filter(is_handcrafted=True)
#             elif is_handcrafted.lower() == 'false':
#                 queryset = queryset.filter(is_handcrafted=False)

#         return queryset
    
# class ProductSearchAPIView(ListAPIView):
#     authentication_classes = [CombinedJWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = ProductSerializer

#     def get_queryset(self):
#         query = self.request.query_params.get('q', None)
#         is_handcrafted = self.request.query_params.get('is_handcrafted', None)
#         min_price = self.request.query_params.get('min_price')
#         max_price = self.request.query_params.get('max_price')

#         queryset = Product.objects.all()

#         if query:
#             queryset = queryset.filter(
#                 Q(head__icontains=query) |
#                 Q(category__name__icontains=query) |
#                 Q(metal__name__icontains=query) |
#                 Q(metal__material__name__icontains=query) |
#                 Q(stones__name__icontains=query)
#             ).distinct()

#         if is_handcrafted is not None:
#             if is_handcrafted.lower() == 'true':
#                 queryset = queryset.filter(is_handcrafted=True)
#             elif is_handcrafted.lower() == 'false':
#                 queryset = queryset.filter(is_handcrafted=False)

#         # Price range filtering using frozen_unit_price
#         if min_price:
#             try:
#                 queryset = queryset.filter(frozen_unit_price__gte=float(min_price))
#             except ValueError:
#                 pass  # Ignore invalid min_price

#         if max_price:
#             try:
#                 queryset = queryset.filter(frozen_unit_price__lte=float(max_price))
#             except ValueError:
#                 pass  # Ignore invalid max_price

#         return queryset

class ProductSearchAPIView(ListAPIView):
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        is_handcrafted = self.request.query_params.get('is_handcrafted', None)
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        queryset = Product.objects.all()

        if query:
            queryset = queryset.filter(
                Q(head__icontains=query) |
                Q(category__name__icontains=query) |
                Q(metal__name__icontains=query) |
                Q(metal__material__name__icontains=query) |
                Q(stones__name__icontains=query)
            ).distinct()

        if is_handcrafted is not None:
            if is_handcrafted.lower() == 'true':
                queryset = queryset.filter(is_handcrafted=True)
            elif is_handcrafted.lower() == 'false':
                queryset = queryset.filter(is_handcrafted=False)

        if min_price:
            try:
                queryset = queryset.filter(frozen_unit_price__gte=float(min_price))
            except ValueError:
                pass

        if max_price:
            try:
                queryset = queryset.filter(frozen_unit_price__lte=float(max_price))
            except ValueError:
                pass

        return queryset


# class ProductSearchAPIView(APIView):
#     authentication_classes = [CombinedJWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         # Example gif URL (you can make this dynamic if you want)
#         gif_url = "http://res.cloudinary.com/dvllntzo0/image/upload/v1749821189/b04x42fkkfw20vkyesgx.webp"

#         # For categories, just empty lists for now (you can replace with real queries)
#         suggested_categories = []
#         popular_categories = []

#         # For suggested products, reuse your serializer and queryset from your ProductSearchAPIView logic
#         from .models import Product
#         from .serializers import ProductSearchSerializer

#         # Example: get some products (or your filtered queryset)
#         products_qs = Product.objects.all()[:5]  # or your custom queryset

#         serializer = ProductSearchSerializer(products_qs, many=True)

#         # popular products example (empty or your logic)
#         popular_products = []

#         return Response({
#             "gif": gif_url,
#             "suggested_categories": suggested_categories,
#             "popular_categories": popular_categories,
#             "suggested_products": serializer.data,
#             "popular_products": popular_products
#         })








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
from django.core.exceptions import ImproperlyConfigured

if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, ADMIN_WHATSAPP_NUMBER]):
    raise ImproperlyConfigured("One or more Twilio environment variables are missing.")

class ProductEnquiryAPIView(APIView):
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]
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
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]

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
        days = int(self.request.query_params.get('days', 30))
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
    


# class ProductListByGender(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, *args, **kwargs):
#         return self.handle_filter(request)

#     def post(self, request, *args, **kwargs):
#         return self.handle_filter(request, use_post=True)

#     def handle_filter(self, request, use_post=False):
#         data = request.data if use_post else request.query_params
#         gender_id = data.get('gender')

#         products = Product.objects.all()
#         if gender_id:
#             products = products.filter(gender_id=gender_id)

#         def parse_list(key):
#             if hasattr(data, 'getlist'):
#                 return [v for v in data.getlist(key) if v]
#             val = data.get(key)
#             if isinstance(val, list):
#                 return val
#             elif isinstance(val, str):
#                 return [v.strip() for v in val.split(',') if v.strip()]
#             return []

#         # Parse filters
#         subcategories = parse_list('subcategory')
#         materials = parse_list('materials')
#         gemstones = parse_list('gemstones')
#         colors = parse_list('colors')
#         brand = data.get('brand', '').strip()
#         price_raw = data.get('price')

#         # Parse price
#         price_min = price_max = None
#         try:
#             if isinstance(price_raw, str) and '-' in price_raw:
#                 price_min, price_max = map(float, price_raw.split('-'))
#             elif isinstance(price_raw, dict):
#                 price_min = float(price_raw.get('min', 0))
#                 price_max = float(price_raw.get('max', 1000000))
#             elif isinstance(price_raw, str) and price_raw.strip().startswith('{'):
#                 price_dict = json.loads(price_raw)
#                 price_min = float(price_dict.get("min", 0))
#                 price_max = float(price_dict.get("max", 1000000))
#         except Exception:
#             price_min = price_max = None

#         # Apply filters
#         if subcategories:
#             products = products.filter(Subcategories__sub_name__in=subcategories)
#         if brand:
#             products = products.filter(head__icontains=brand)
#         if materials:
#             products = products.filter(metal__material__name__in=materials)
#         if gemstones:
#             products = products.filter(productstone__stone__name__in=gemstones).distinct()
#         if colors:
#             products = products.filter(metal__color__in=colors)

#         # Final price filter
#         filtered_products = []
#         for product in products:
#             try:
#                 gt = float(product.grand_total)
#                 if price_min is not None and gt < price_min:
#                     continue
#                 if price_max is not None and gt > price_max:
#                     continue
#                 filtered_products.append(product)
#             except:
#                 continue

#         serializer = ProductSerializer(filtered_products, many=True)

#         # Build filter metadata
#         gender = Gender.objects.filter(id=gender_id).first() if gender_id else None
#         gender_name = gender.name if gender else "All"

#         if filtered_products:
#             prices = [float(p.grand_total) for p in filtered_products]
#             price_range = {
#                 "min": min(prices),
#                 "max": max(prices)
#             }
#         else:
#             price_range = {
#                 "min": 0,
#                 "max": 0
#             }

#         metal_colors = Metal.objects.values_list("color", flat=True).distinct()
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

#         # Subcategories related to gender
#         subcategory_ids = Product.objects.filter(gender_id=gender_id).values_list("Subcategories__id", flat=True).distinct()
#         subcategories_qs = Subcategories.objects.filter(id__in=subcategory_ids).values("id", "sub_name")

#         filter_category_data = [{
#             "category": {
#                 "id": gender.id if gender else None,
#                 "name": gender_name
#             },
#             "subcategories": list(subcategories_qs),
#             "price_range": price_range,
#             "brand": "my jewelry my design",
#             "materials": list(Material.objects.all().values("id", "name")),
#             "gemstones": list(Gemstone.objects.all().values("id", "name")),
#             "colors": colors_with_codes
#         }]

#         message = None
#         if any([subcategories, materials, gemstones, colors, brand, price_raw]):
#             message = "Filters Applied" if filtered_products else "No Matching Filters"

#         return Response({
#             "gender": gender_name,
#             "products": serializer.data,
#             "filter_category": filter_category_data,
#             "message": message
#         })







# class ProductListByGender(APIView):
#     def get_filter_data(self, products):
#         grand_totals = [p.grand_total for p in products if p.grand_total is not None]
#         min_price = float(min(grand_totals)) if grand_totals else 0.0
#         max_price = float(max(grand_totals)) if grand_totals else 0.0

#         materials = Metal.objects.filter(id__in=products.values_list('metal_id', flat=True)).distinct()
#         material_data = [{"id": m.id, "name": m.name} for m in materials]

#         gemstones = Gemstone.objects.filter(products__in=products).distinct()
#         gemstone_data = [{"id": g.id, "name": g.name} for g in gemstones]

#         categories = products.values('category__id', 'category__name').distinct()
#         category_list = [{"id": c["category__id"], "name": c["category__name"]} for c in categories]

#         colors = [
#             {"color": "Yellow", "code": "#ffff00"},
#             {"color": "Red", "code": "#ff0000"}
#         ]

#         return [{
#             "category": category_list,
#             "price_range": {
#                 "min": min_price,
#                 "max": max_price
#             },
#             "brand": "my jewelry my design",
#             "materials": material_data,
#             "gemstones": gemstone_data,
#             "colors": colors
#         }]

#     def get(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)
#         filter_category = self.get_filter_data(products)
#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)

#     def post(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)

#         # FORM DATA FILTERS
#         category_name = request.POST.get("category")
#         subcategory_name = request.POST.get("subcategory")
#         material_name = request.POST.get("material")
#         gemstone_name = request.POST.get("gemstone")
#         min_price = request.POST.get("min_price")
#         max_price = request.POST.get("max_price")

#         if category_name:
#             products = products.filter(category__name__iexact=category_name)

#         if subcategory_name:
#             products = products.filter(subcategory__sub_name__iexact=subcategory_name)

#         if material_name:
#             products = products.filter(metal__name__iexact=material_name)

#         if gemstone_name:
#             products = products.filter(gemstone__name__iexact=gemstone_name)

#         if min_price and max_price:
#             try:
#                 min_p = float(min_price)
#                 max_p = float(max_price)
#                 products = [p for p in products if p.grand_total and min_p <= p.grand_total <= max_p]
#             except ValueError:
#                 pass

#         filter_category = self.get_filter_data(Product.objects.filter(gender=gender))
#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)

# class ProductListByGender(APIView):
#     def get_filter_data(self, products):
#         grand_totals = [p.grand_total for p in products if p.grand_total is not None]
#         min_price = float(min(grand_totals)) if grand_totals else 0.0
#         max_price = float(max(grand_totals)) if grand_totals else 0.0

#         materials = Metal.objects.filter(id__in=products.values_list('metal_id', flat=True)).distinct()
#         material_data = [{"id": m.id, "name": m.name} for m in materials]

#         gemstones = Gemstone.objects.filter(products__in=products).distinct()
#         gemstone_data = [{"id": g.id, "name": g.name} for g in gemstones]

#         categories = products.values('category__id', 'category__name').distinct()
#         category_list = [{"id": c["category__id"], "name": c["category__name"]} for c in categories]

#         colors = [
#             {"color": "Yellow", "code": "#ffff00"},
#             {"color": "Red", "code": "#ff0000"}
#         ]

#         return [{
#             "category": category_list,
#             "price_range": {
#                 "min": min_price,
#                 "max": max_price
#             },
#             "brand": "my jewelry my design",
#             "materials": material_data,
#             "gemstones": gemstone_data,
#             "colors": colors
#         }]

#     def get(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)
#         filter_category = self.get_filter_data(products)
#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)

#     def post(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)

#         # FORM-DATA FIELDS
#         category_name = request.POST.get("category")
#         subcategory_name = request.POST.get("subcategory")
#         material_name = request.POST.get("material")
#         gemstone_name = request.POST.get("gemstone")
#         price_json = request.POST.get("price")

#         if category_name:
#             products = products.filter(category__name__iexact=category_name)

#         if subcategory_name:
#             products = products.filter(subcategory__sub_name__iexact=subcategory_name)

#         if material_name:
#             products = products.filter(metal__name__iexact=material_name)

#         if gemstone_name:
#             products = products.filter(gemstone__name__iexact=gemstone_name)

#         if price_json:
#             try:
#                 price_data = json.loads(price_json)
#                 min_price = float(price_data.get("min", 0))
#                 max_price = float(price_data.get("max", 1e10))
#                 products = [p for p in products if p.grand_total and min_price <= p.grand_total <= max_price]
#             except (ValueError, json.JSONDecodeError):
#                 pass

#         filter_category = self.get_filter_data(Product.objects.filter(gender=gender))
#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)



# class ProductListByGender(APIView):
#     def get_filter_data(self, products):
#         grand_totals = [p.grand_total for p in products if p.grand_total is not None]
#         min_price = float(min(grand_totals)) if grand_totals else 0.0
#         max_price = float(max(grand_totals)) if grand_totals else 0.0

#         materials = Metal.objects.filter(id__in=products.values_list('metal_id', flat=True)).distinct()
#         material_data = [{"id": m.id, "name": m.name} for m in materials]

#         gemstones = Gemstone.objects.filter(products__in=products).distinct()
#         gemstone_data = [{"id": g.id, "name": g.name} for g in gemstones]

#         categories = products.values('category__id', 'category__name').distinct()
#         category_list = [{"id": c["category__id"], "name": c["category__name"]} for c in categories]

#         # ✅ Dynamically fetch metal colors
#         metal_colors = Metal.objects.filter(id__in=products.values_list('metal_id', flat=True))\
#                                     .exclude(color__isnull=True).exclude(color__exact="")\
#                                     .values_list('color', flat=True).distinct()
#         color_data = [{"color": color, "code": "#cccccc"} for color in metal_colors]  # Default color code for now

#         return [{
#             "category": category_list,
#             "price_range": {
#                 "min": min_price,
#                 "max": max_price
#             },
#             "brand": "my jewelry my design",
#             "materials": material_data,
#             "gemstones": gemstone_data,
#             "colors": color_data
#         }]

#     def get(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)
#         filter_category = self.get_filter_data(products)
#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)

#     def post(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)

#         # FORM-DATA FIELDS
#         category_name = request.POST.get("category")
#         subcategory_name = request.POST.get("subcategory")
#         material_name = request.POST.get("material")
#         gemstone_name = request.POST.get("gemstone")
#         color_name = request.POST.get("color")
#         price_json = request.POST.get("price")

#         if category_name:
#             products = products.filter(category__name__iexact=category_name)

#         if subcategory_name:
#             products = products.filter(subcategory__sub_name__iexact=subcategory_name)

#         if material_name:
#             products = products.filter(metal__name__iexact=material_name)

#         if gemstone_name:
#             products = products.filter(gemstone__name__iexact=gemstone_name)

#         if color_name:
#             products = products.filter(metal__color__iexact=color_name)

#         if price_json:
#             try:
#                 price_data = json.loads(price_json)
#                 min_price = float(price_data.get("min", 0))
#                 max_price = float(price_data.get("max", 1e10))
#                 products = [p for p in products if p.grand_total and min_price <= p.grand_total <= max_price]
#             except (ValueError, json.JSONDecodeError):
#                 pass

#         filter_category = self.get_filter_data(Product.objects.filter(gender=gender))
#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)


# class ProductListByGender(APIView):
#     def get_filter_data(self, products, clear=False):
#         if not isinstance(products, models.QuerySet):
#             products = Product.objects.filter(id__in=[p.id for p in products])

#         grand_totals = [p.grand_total for p in products if p.grand_total is not None]
#         min_price = float(min(grand_totals)) if grand_totals else 0.0
#         max_price = float(max(grand_totals)) if grand_totals else 0.0

#         materials = Metal.objects.filter(id__in=products.values_list('metal_id', flat=True)).distinct()
#         material_data = [{"id": m.id, "name": m.name} for m in materials]

#         gemstones = Gemstone.objects.filter(products__in=products).distinct()
#         gemstone_data = [{"id": g.id, "name": g.name} for g in gemstones]

#         categories = products.values('category__id', 'category__name').distinct()
#         category_list = [{"id": c["category__id"], "name": c["category__name"]} for c in categories]

#         metal_colors = Metal.objects.filter(id__in=products.values_list('metal_id', flat=True))\
#                                     .exclude(color__isnull=True).exclude(color__exact="")\
#                                     .values_list('color', flat=True).distinct()
#         color_data = [{"color": color, "code": "#cccccc"} for color in metal_colors]

#         return [{
#             "category": category_list,
#             "price_range": {
#                 "min": min_price,
#                 "max": max_price
#             },
#             "brand": "my jewelry my design",
#             "materials": material_data,
#             "gemstones": gemstone_data,
#             "colors": color_data,
#             "clear": clear
#         }]

#     def get(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)
#         filter_category = self.get_filter_data(products, clear=True)
#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)

#     def post(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)

#         category_name = request.POST.get("category")
#         subcategory_name = request.POST.get("subcategory")
#         material_name = request.POST.get("material")
#         gemstone_name = request.POST.get("gemstone")
#         color_name = request.POST.get("color")
#         price_json = request.POST.get("price")

#         filters_applied = False

#         if category_name:
#             products = products.filter(category__name__iexact=category_name)
#             filters_applied = True

#         if subcategory_name:
#             products = products.filter(subcategory__sub_name__iexact=subcategory_name)
#             filters_applied = True

#         if material_name:
#             products = products.filter(metal__name__iexact=material_name)
#             filters_applied = True

#         if gemstone_name:
#             products = products.filter(gemstone__name__iexact=gemstone_name)
#             filters_applied = True

#         if color_name:
#             products = products.filter(metal__color__iexact=color_name)
#             filters_applied = True

#         if price_json:
#             try:
#                 price_data = json.loads(price_json)
#                 min_price = float(price_data.get("min", 0))
#                 max_price = float(price_data.get("max", 1e10))
#                 products = [p for p in products if p.grand_total and min_price <= p.grand_total <= max_price]
#                 filters_applied = True
#             except (ValueError, json.JSONDecodeError):
#                 return Response({"error": "Invalid price format."}, status=status.HTTP_400_BAD_REQUEST)

#         filter_category = self.get_filter_data(products if isinstance(products, list) else products.all(), clear=not filters_applied)
#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)
# class ProductListByGender(APIView):
#     def get_filter_data(self, products, clear=False):
#         if not isinstance(products, models.QuerySet):
#             products = Product.objects.filter(id__in=[p.id for p in products])

#         grand_totals = [p.grand_total for p in products if p.grand_total is not None]
#         min_price = float(min(grand_totals)) if grand_totals else 0.0
#         max_price = float(max(grand_totals)) if grand_totals else 0.0

#         materials = Metal.objects.filter(id__in=products.values_list('metal_id', flat=True)).distinct()
#         material_data = [{"id": m.id, "name": m.name} for m in materials]

#         gemstones = Gemstone.objects.filter(products__in=products).distinct()
#         gemstone_data = [{"id": g.id, "name": g.name} for g in gemstones]

#         categories = products.values('category__id', 'category__name').distinct()
#         category_list = [{"id": c["category__id"], "name": c["category__name"]} for c in categories]

#         metal_colors = Metal.objects.filter(id__in=products.values_list('metal_id', flat=True))\
#                                     .exclude(color__isnull=True).exclude(color__exact="")\
#                                     .values_list('color', flat=True).distinct()
#         color_data = [{"color": color, "code": "#cccccc"} for color in metal_colors]

#         return [{
#             "category": category_list,
#             "price_range": {
#                 "min": min_price,
#                 "max": max_price
#             },
#             "brand": "my jewelry my design",
#             "materials": material_data,
#             "gemstones": gemstone_data,
#             "colors": color_data,
#             "clear": clear
#         }]

#     def get(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)
#         filter_category = self.get_filter_data(products, clear=True)
#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)

#     def post(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)

#         # Collect filters from form-data
#         category_name = request.POST.get("category")
#         subcategory_name = request.POST.get("subcategory")
#         material_name = request.POST.get("material")
#         gemstone_name = request.POST.get("gemstone")
#         color_name = request.POST.get("color")
#         price_json = request.POST.get("price")

#         filters_applied = False

#         if category_name:
#             products = products.filter(category__name__iexact=category_name)
#             filters_applied = True

#         if subcategory_name:
#             products = products.filter(subcategory__sub_name__iexact=subcategory_name)
#             filters_applied = True

#         if material_name:
#             products = products.filter(metal__name__iexact=material_name)
#             filters_applied = True

#         if gemstone_name:
#             products = products.filter(gemstone__name__iexact=gemstone_name)
#             filters_applied = True

#         if color_name:
#             products = products.filter(metal__color__iexact=color_name)
#             filters_applied = True

#         if price_json:
#             try:
#                 price_data = json.loads(price_json)
#                 min_price = float(price_data.get("min", 0))
#                 max_price = float(price_data.get("max", 1e10))
#                 products = [p for p in products if p.grand_total and min_price <= p.grand_total <= max_price]
#                 filters_applied = True
#             except (ValueError, json.JSONDecodeError):
#                 return Response({"error": "Invalid price format."}, status=status.HTTP_400_BAD_REQUEST)

#         filter_category = self.get_filter_data(
#             products if isinstance(products, list) else products.all(),
#             clear=not filters_applied
#         )

#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)


# class ProductListByGender(APIView):
#     def get_filter_data(self, products, clear=False):
#         if not isinstance(products, models.QuerySet):
#             products = Product.objects.filter(id__in=[p.id for p in products])

#         grand_totals = [p.grand_total for p in products if p.grand_total is not None]
#         min_price = float(min(grand_totals)) if grand_totals else 0.0
#         max_price = float(max(grand_totals)) if grand_totals else 0.0

#         materials = Metal.objects.filter(id__in=products.values_list('metal_id', flat=True)).distinct()
#         material_data = [{"id": m.id, "name": m.name} for m in materials]

#         gemstones = Gemstone.objects.filter(products__in=products).distinct()
#         gemstone_data = [{"id": g.id, "name": g.name} for g in gemstones]

#         categories = products.values('category__id', 'category__name').distinct()
#         category_list = [{"id": c["category__id"], "name": c["category__name"]} for c in categories]

#         metal_colors = Metal.objects.filter(id__in=products.values_list('metal_id', flat=True))\
#             .exclude(color__isnull=True).exclude(color__exact="")\
#             .values_list('color', flat=True).distinct()
#         color_data = [{"color": color, "code": "#cccccc"} for color in metal_colors]

#         return [{
#             "category": category_list,
#             "price_range": {
#                 "min": min_price,
#                 "max": max_price
#             },
#             "brand": "my jewelry my design",
#             "materials": material_data,
#             "gemstones": gemstone_data,
#             "colors": color_data,
#             "clear": clear
#         }]

#     def get(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)
#         filter_category = self.get_filter_data(products, clear=True)
#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)

#     def post(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)
#         original_products = products  # For fallback filter data

#         filters_applied = False

#         category_name = request.POST.get("category")
#         subcategory_name = request.POST.get("subcategory")
#         material_name = request.POST.get("material")
#         gemstone_name = request.POST.get("gemstone")
#         color_name = request.POST.get("color")
#         price_json = request.POST.get("price")

#         if category_name:
#             products = products.filter(category__name__iexact=category_name)
#             filters_applied = True

#         if subcategory_name:
#             products = products.filter(subcategory__sub_name__iexact=subcategory_name)
#             filters_applied = True

#         if material_name:
#             products = products.filter(metal__name__iexact=material_name)
#             filters_applied = True

#         if gemstone_name:
#             products = products.filter(gemstone__name__iexact=gemstone_name)
#             filters_applied = True

#         if color_name:
#             products = products.filter(metal__color__iexact=color_name)
#             filters_applied = True

#         if price_json:
#             try:
#                 price_data = json.loads(price_json)
#                 min_price = float(price_data.get("min", 0))
#                 max_price = float(price_data.get("max", 1e10))
#                 products = [p for p in products if p.grand_total and min_price <= p.grand_total <= max_price]
#                 filters_applied = True
#             except (ValueError, json.JSONDecodeError):
#                 return Response({"error": "Invalid price format."}, status=status.HTTP_400_BAD_REQUEST)

#         # If filtered result is a list, convert to queryset
#         if isinstance(products, list):
#             products_qs = Product.objects.filter(id__in=[p.id for p in products])
#         else:
#             products_qs = products

#         filter_category = self.get_filter_data(
#             products_qs,
#             clear=not filters_applied
#         )

#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)


# class ProductListByGender(APIView):
#     def get_filter_data(self, products):
#         grand_totals = [float(p.grand_total) for p in products if p.grand_total is not None]
#         min_price = min(grand_totals) if grand_totals else 0
#         max_price = max(grand_totals) if grand_totals else 0

#         materials = Material.objects.filter(id__in=products.values_list('metal__material_id', flat=True)).values('id', 'name').distinct()
#         gemstones = Gemstone.objects.filter(productstone__product__in=products).values('id', 'name').distinct()
#         metal_colors = Metal.objects.filter(id__in=products.values_list('metal_id', flat=True)).values_list("color", flat=True).distinct()

#         colors_with_codes = []
#         for color in metal_colors:
#             color_name = str(color).strip().lower()
#             try:
#                 hex_code = name_to_hex(color_name)
#             except ValueError:
#                 hex_code = "#CCCCCC"
#             colors_with_codes.append({"color": color, "code": hex_code})

#         subcategories = Subcategories.objects.filter(category__in=products.values_list('category_id', flat=True)).values("id", "sub_name").distinct()

#         categories = products.values('category__id', 'category__name').distinct()
#         category_list = [{"id": c["category__id"], "name": c["category__name"]} for c in categories]

#         return {
#             "price_range": {"min": min_price, "max": max_price},
#             "materials": list(materials),
#             "gemstones": list(gemstones),
#             "colors": colors_with_codes,
#             "subcategories": list(subcategories),
#             "categories": category_list,
#             "brand": "my jewelry my design"
#         }

#     def get(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)
#         filter_category = self.get_filter_data(products, clear=True)
#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)

#     def post(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)

#         # Detect if clear is explicitly requested
#         clear_flag = request.POST.get("clear", "false").lower() == "true"

#         # If clear is true, skip applying filters
#         if clear_flag:
#             filter_category = self.get_filter_data(products, clear=True)
#             serialized_products = ProductSerializer(products, many=True).data
#             return Response({
#                 "filter_category": filter_category,
#                 "products": serialized_products
#             }, status=status.HTTP_200_OK)

#         # Otherwise, apply filters normally
#         filters_applied = False

#         category_name = request.POST.get("category")
#         subcategory_name = request.POST.get("subcategory")
#         material_name = request.POST.get("material")
#         gemstone_name = request.POST.get("gemstone")
#         color_name = request.POST.get("color")
#         price_json = request.POST.get("price")

#         if category_name:
#             products = products.filter(category__name__iexact=category_name)
#             filters_applied = True

#         if subcategory_name:
#             products = products.filter(subcategory__sub_name__iexact=subcategory_name)
#             filters_applied = True

#         if material_name:
#             products = products.filter(metal__name__iexact=material_name)
#             filters_applied = True

#         if gemstone_name:
#             products = products.filter(gemstone__name__iexact=gemstone_name)
#             filters_applied = True

#         if color_name:
#             products = products.filter(metal__color__iexact=color_name)
#             filters_applied = True

#         if price_json:
#             try:
#                 price_data = json.loads(price_json)
#                 min_price = float(price_data.get("min", 0))
#                 max_price = float(price_data.get("max", 1e10))
#                 products = [p for p in products if p.grand_total and min_price <= p.grand_total <= max_price]
#                 filters_applied = True
#             except (ValueError, json.JSONDecodeError):
#                 return Response({"error": "Invalid price format."}, status=status.HTTP_400_BAD_REQUEST)

#         if isinstance(products, list):
#             products_qs = Product.objects.filter(id__in=[p.id for p in products])
#         else:
#             products_qs = products

#         filter_category = self.get_filter_data(products_qs, clear=not filters_applied)
#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)

# class ProductListByGender(APIView):
#     permission_classes = [AllowAny]

#     def get_filter_data(self, products):
#         grand_totals = [float(p.grand_total) for p in products if p.grand_total is not None]
#         min_price = min(grand_totals) if grand_totals else 0
#         max_price = max(grand_totals) if grand_totals else 0

#         materials = Material.objects.filter(
#             id__in=products.values_list('metal__material_id', flat=True)
#         ).values('id', 'name').distinct()

#         gemstones = Gemstone.objects.filter(
#             productstone__product__in=products
#         ).values('id', 'name').distinct()

#         metal_colors = Metal.objects.filter(
#             id__in=products.values_list('metal_id', flat=True)
#         ).values_list("color", flat=True).distinct()

#         colors_with_codes = []
#         for color in metal_colors:
#             color_name = str(color).strip().lower()
#             try:
#                 hex_code = name_to_hex(color_name)
#             except ValueError:
#                 hex_code = "#CCCCCC"
#             colors_with_codes.append({"color": color, "code": hex_code})

#         # subcategories = Subcategories.objects.filter(
#         #     category__in=products.values_list('category_id', flat=True)
#         # ).values("id", "sub_name").distinct()

#         categories = products.values('category__id', 'category__name').distinct()
#         category_list = [{"id": c["category__id"], "sub_name": c["category__name"]} for c in categories]

#         return {
#             "price_range": {"min": min_price, "max": max_price},
#             "materials": list(materials),
#             "gemstones": list(gemstones),
#             "colors": colors_with_codes,
#             # "subcategories": list(subcategories),
#             "subcategories": category_list,
#             "brand": "my jewelry my design"
#         }

#     def get(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)
#         filter_category = self.get_filter_data(products)
#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)

#     def post(self, request, gender_id=None):
#         try:
#             gender = Gender.objects.get(id=gender_id)
#         except Gender.DoesNotExist:
#             return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

#         products = Product.objects.filter(gender=gender)

#         clear_flag = request.data.get("clear", False)
#         if isinstance(clear_flag, str):
#             clear_flag = clear_flag.lower() == "true"

#         if clear_flag:
#             filter_category = self.get_filter_data(products)
#             serialized_products = ProductSerializer(products, many=True).data
#             return Response({
#                 "filter_category": filter_category,
#                 "products": serialized_products
#             }, status=status.HTTP_200_OK)

#         # Apply filters
#         category_name = request.data.get("category")
#         # subcategory_name = request.data.get("subcategory")
#         material_name = request.data.get("material")
#         gemstone_name = request.data.get("gemstone")
#         color_name = request.data.get("color")
#         price_json = request.data.get("price")

#         if category_name:
#             products = products.filter(category__name__iexact=category_name)

#         # if subcategory_name:
#         #     products = products.filter(subcategory__sub_name__iexact=subcategory_name)

#         if material_name:
#             # Assuming Material name filter is related via metal__material__name
#             products = products.filter(metal__material__name__iexact=material_name)

#         if gemstone_name:
#             # Assuming relation via productstone__stone__name
#             products = products.filter(productstone__stone__name__iexact=gemstone_name)

#         if color_name:
#             products = products.filter(metal__color__iexact=color_name)

#         if price_json:
#             try:
#                 price_data = json.loads(price_json)
#                 min_price = float(price_data.get("min", 0))
#                 max_price = float(price_data.get("max", 1e10))
#                 products = products.filter(grand_total__gte=min_price, grand_total__lte=max_price)
#             except (ValueError, json.JSONDecodeError):
#                 return Response({"error": "Invalid price format."}, status=status.HTTP_400_BAD_REQUEST)

#         filter_category = self.get_filter_data(products)
#         serialized_products = ProductSerializer(products, many=True).data

#         return Response({
#             "filter_category": filter_category,
#             "products": serialized_products
#         }, status=status.HTTP_200_OK)


class ProductListByGender(APIView):
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_filter_data(self, products_qs):
        """
        Accepts a queryset to avoid .values_list errors from Python lists.
        """
        grand_totals = [float(p.grand_total) for p in products_qs if p.grand_total is not None]
        min_price = min(grand_totals) if grand_totals else 0
        max_price = max(grand_totals) if grand_totals else 0

        # Use only if it's still a queryset
        materials = Material.objects.filter(
            id__in=products_qs.values_list('metal__material__id', flat=True)
        ).values('id', 'name').distinct()

        gemstones = Gemstone.objects.filter(
            productstone__product__in=products_qs
        ).values('id', 'name').distinct()

        metal_colors = Metal.objects.filter(
            id__in=products_qs.values_list('metal_id', flat=True)
        ).values_list("color", flat=True).distinct()

        colors_with_codes = []
        for color in metal_colors:
            color_name = str(color).strip().lower()
            try:
                hex_code = name_to_hex(color_name)
            except ValueError:
                hex_code = "#CCCCCC"
            colors_with_codes.append({"color": color, "code": hex_code})

        categories = products_qs.values('category__id', 'category__name').distinct()
        category_list = [{"id": c["category__id"], "sub_name": c["category__name"]} for c in categories]

        return {
            "price_range": {"min": min_price, "max": max_price},
            "materials": list(materials),
            "gemstones": list(gemstones),
            "colors": colors_with_codes,
            "subcategories": category_list,
            "brand": "my jewelry my design"
        }

    def get(self, request, gender_id=None):
        try:
            gender = Gender.objects.get(id=gender_id)
        except Gender.DoesNotExist:
            return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

        products_qs = Product.objects.filter(gender=gender)
        filter_category = self.get_filter_data(products_qs)
        serialized_products = ProductSerializer(products_qs, many=True).data

        return Response({
            "filter_category": filter_category,
            "products": serialized_products
        }, status=status.HTTP_200_OK)

    def post(self, request, gender_id=None):
        try:
            gender = Gender.objects.get(id=gender_id)
        except Gender.DoesNotExist:
            return Response({"error": "Gender not found."}, status=status.HTTP_404_NOT_FOUND)

        products_qs = Product.objects.filter(gender=gender)

        clear_flag = request.data.get("clear", False)
        if isinstance(clear_flag, str):
            clear_flag = clear_flag.lower() == "true"

        if clear_flag:
            filter_category = self.get_filter_data(products_qs)
            serialized_products = ProductSerializer(products_qs, many=True).data
            return Response({
                "filter_category": filter_category,
                "products": serialized_products
            }, status=status.HTTP_200_OK)

        # Apply filters
        category_name = request.data.get("category")
        material_name = request.data.get("material")
        gemstone_name = request.data.get("gemstone")
        color_name = request.data.get("color")
        price_json = request.data.get("price")

        if category_name:
            products_qs = products_qs.filter(category__name__iexact=category_name)

        if material_name:
            products_qs = products_qs.filter(metal__material__name__iexact=material_name)

        if gemstone_name:
            products_qs = products_qs.filter(productstone__stone__name__iexact=gemstone_name)

        if color_name:
            products_qs = products_qs.filter(metal__color__iexact=color_name)

        # Handle price filtering in Python since grand_total is not a DB field
        if price_json:
            try:
                price_data = json.loads(price_json)
                min_price = float(price_data.get("min", 0))
                max_price = float(price_data.get("max", 1e10))

                filtered_products = []
                for product in products_qs:
                    try:
                        grand_total = float(product.grand_total)
                        if min_price <= grand_total <= max_price:
                            filtered_products.append(product)
                    except (TypeError, ValueError, AttributeError):
                        continue

                # Now filtered_products is a list, not a queryset
                filter_category = self.get_filter_data(Product.objects.filter(id__in=[p.id for p in filtered_products]))
                serialized_products = ProductSerializer(filtered_products, many=True).data

                return Response({
                    "filter_category": filter_category,
                    "products": serialized_products
                }, status=status.HTTP_200_OK)

            except (ValueError, json.JSONDecodeError):
                return Response({"error": "Invalid price format."}, status=status.HTTP_400_BAD_REQUEST)

        # No price filtering applied
        filter_category = self.get_filter_data(products_qs)
        serialized_products = ProductSerializer(products_qs, many=True).data

        return Response({
            "filter_category": filter_category,
            "products": serialized_products
        }, status=status.HTTP_200_OK)



# class ProductListByGender(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, gender_id):
#         user_id = request.query_params.get("user_id")
#         wishlist_items = []

#         if user_id:
#             try:
#                 user = Register.objects.get(pk=user_id)
#                 wishlist_items = Wishlist.objects.filter(user=user).values_list("product_id", flat=True)
#             except Register.DoesNotExist:
#                 return Response({"error": "Invalid user_id"}, status=status.HTTP_400_BAD_REQUEST)

#         products = Product.objects.filter(gender_id=gender_id)
#         serializer = ProductSerializer(products, many=True, context={"wishlist_items": wishlist_items})
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, gender_id):
#         user_id = request.data.get("user_id")
#         subcategory_ids = request.data.get("subcategory_ids", [])
#         min_price = request.data.get("min_price")
#         max_price = request.data.get("max_price")
#         materials = request.data.get("materials", [])
#         gemstones = request.data.get("gemstones", [])
#         colors = request.data.get("colors", [])
#         brand = request.data.get("brand", None)

#         wishlist_items = []
#         if user_id:
#             try:
#                 user = Register.objects.get(pk=user_id)
#                 wishlist_items = Wishlist.objects.filter(user=user).values_list("product_id", flat=True)
#             except Register.DoesNotExist:
#                 return Response({"error": "Invalid user_id"}, status=status.HTTP_400_BAD_REQUEST)

#         filters = Q(gender_id=gender_id)

#         if subcategory_ids:
#             filters &= Q(category_id__in=subcategory_ids) | Q(occasion_id__in=subcategory_ids)
#         if materials:
#             filters &= Q(metal__material__id__in=materials)
#         if gemstones:
#             filters &= Q(productstone__stone__id__in=gemstones)
#         if colors:
#             color_names = [c["color"] for c in colors if "color" in c]
#             filters &= Q(color__in=color_names)
#         if brand:
#             filters &= Q(brand__iexact=brand)

#         products = Product.objects.filter(filters).distinct()
#         serialized_products = ProductSerializer(products, many=True, context={"wishlist_items": wishlist_items}).data

#         # Filter grand_total by price
#         if min_price is not None and max_price is not None:
#             try:
#                 min_price = float(min_price)
#                 max_price = float(max_price)
#                 serialized_products = [
#                     product for product in serialized_products
#                     if min_price <= float(product.get("grand_total", 0)) <= max_price
#                 ]
#             except ValueError:
#                 return Response({"error": "Invalid price values"}, status=status.HTTP_400_BAD_REQUEST)

#         # Prepare filter_category response
#         filter_category = {
#             "price_range": {
#                 "min": min_price,
#                 "max": max_price
#             },
#             "materials": [{"id": m, "name": "Material"} for m in materials],
#             "gemstones": [{"id": g, "name": "Gemstone"} for g in gemstones],
#             "colors": colors,
#             "subcategories": [{"id": s, "sub_name": "Subcategory"} for s in subcategory_ids],
#             "brand": brand,
#         }

#         return Response({
#             "products": serialized_products,
#             "filter_category": filter_category
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



# class SevenCategoryDetailAPIView(APIView):
#     authentication_classes = [CombinedJWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]

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

#             # Parse filters
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

#             # Parse price filter (object or string)
#             try:
#                 if isinstance(price_raw, str) and "-" in price_raw:
#                     price_min, price_max = map(float, price_raw.split("-"))
#                 elif isinstance(price_raw, dict):
#                     price_min = float(price_raw.get("min", 0))
#                     price_max = float(price_raw.get("max", 1000000))
#                 elif isinstance(price_raw, str) and price_raw.strip().startswith("{"):
#                     import json
#                     price_dict = json.loads(price_raw)
#                     price_min = float(price_dict.get("min", 0))
#                     price_max = float(price_dict.get("max", 1000000))
#             except (ValueError, TypeError, json.JSONDecodeError):
#                 price_min = price_max = None

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

#         # Build filtered product list
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
#                 "is_wishlisted": True  # Replace with real logic if needed
#             })

#         # Build price_range from matched products
#         if product_list:
#             all_prices = [float(p["grand_total"]) for p in product_list]
#             price_range = {
#                 "min": min(all_prices),
#                 "max": max(all_prices)
#             }
#         else:
#             price_range = {
#                 "min": 0,
#                 "max": 0
#             }

#         # Filter metadata
#         metal_colors = Metal.objects.values_list("color", flat=True).distinct()
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
#             "subcategories": list(Subcategories.objects.filter(category=category).values("id", "sub_name")),
#             "price_range": price_range,
#             "brand": "my jewelry my design",
#             "materials": list(Material.objects.all().values("id", "name")),
#             "gemstones": list(Gemstone.objects.all().values("id", "name")),
#             "colors": colors_with_codes
#         }]

#         message = None
#         if filter_data and not clear_filter:
#             message = "Filters Applied" if product_list else "No Matching Filters"

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
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

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

        # Prefetch wishlist products to avoid N+1 queries
        user = request.user
        wishlisted_ids = set(
            Wishlist.objects.filter(user=user, product__in=products).values_list('product_id', flat=True)
        )

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
                "is_wishlisted": product.id in wishlisted_ids
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
            { "id": 1, "label": "<25K", "icon": "https://res.cloudinary.com/dadqevs2b/image/upload/v1755512227/Frame_40151_2_fyg5tz.png" },
            { "id": 2, "label": "25K - 50K", "icon": "https://res.cloudinary.com/dadqevs2b/image/upload/v1755512227/Frame_40151_1_mh98bp.png" },
            { "id": 3, "label": "50K - 1L", "icon": "https://res.cloudinary.com/dadqevs2b/image/upload/v1755512227/Frame_40151_3_kluwsu.png" },
            { "id": 4, "label": "1L & Above", "icon": "https://res.cloudinary.com/dadqevs2b/image/upload/v1755512226/Frame_40151_4_f8mmqx.png" },
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







# class CombinedSuggestionsView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         user = request.user if request.user.is_authenticated else None
#         query = request.GET.get('query', '').strip()

#         suggested_categories = []
#         suggested_products = []
#         popular_categories = []
#         popular_products = []

#         if query:
#             # Show suggestions based on query (material or category/product name)
#             material_match = Material.objects.filter(name__icontains=query).first()
#             if material_match:
#                 suggested_categories = Category.objects.filter(
#                     product__metal__material=material_match
#                 ).distinct()
#                 if not suggested_categories.exists():
#                     suggested_categories = Category.objects.filter(name__icontains=query)
#             else:
#                 suggested_categories = Category.objects.filter(name__icontains=query)

#             suggested_products = Product.objects.filter(head__icontains=query)

#         else:
#             # Show popular items when no query is provided
#             pop_cat_ids = (
#                 UserVisit.objects
#                 .values('product__category')
#                 .annotate(visits=Count('id'))
#                 .order_by('-visits')
#                 .values_list('product__category', flat=True)[:5]
#             )
#             popular_categories = Category.objects.filter(id__in=pop_cat_ids) if pop_cat_ids else Category.objects.order_by('?')[:5]

#             pop_prod_ids = (
#                 UserVisit.objects
#                 .values('product')
#                 .annotate(visits=Count('id'))
#                 .order_by('-visits')
#                 .values_list('product', flat=True)[:10]
#             )
#             popular_products = Product.objects.filter(id__in=pop_prod_ids) if pop_prod_ids else Product.objects.order_by('?')[:10]

#         # Optional: Search GIF
#         gif = SearchGif.objects.first()
#         gif_url = gif.image.url if gif else None

#         data = {
#             "gif": gif_url,
#             "suggested_categories": CategoryNameSerializer(suggested_categories, many=True).data,
#             "popular_categories": CategoryNameSerializer(popular_categories, many=True).data,
#             "suggested_products": PopularProductSerializer(suggested_products, many=True).data,
#             "popular_products": PopularProductSerializer(popular_products, many=True).data,
#         }

#         return Response(data)



class CombinedSuggestionsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        query = request.GET.get('q', '').strip()

        suggested_categories = []
        suggested_products = []
        popular_categories = []
        popular_products = []

        if query:
            # Suggested categories
            material_match = Material.objects.filter(name__icontains=query).first()
            if material_match:
                suggested_categories = Category.objects.filter(
                    product__metal__material=material_match
                ).distinct()
                if not suggested_categories.exists():
                    suggested_categories = Category.objects.filter(name__icontains=query)
            else:
                suggested_categories = Category.objects.filter(name__icontains=query)

            # Suggested products
            suggested_products = Product.objects.filter(head__icontains=query)

        else:
            # Popular categories
            pop_cat_ids = (
                UserVisit.objects
                .values('product__category')
                .annotate(visits=Count('id'))
                .order_by('-visits')
                .values_list('product__category', flat=True)[:5]
            )
            popular_categories = Category.objects.filter(id__in=pop_cat_ids) if pop_cat_ids else Category.objects.order_by('?')[:5]

            # Popular products
            pop_prod_ids = (
                UserVisit.objects
                .values('product')
                .annotate(visits=Count('id'))
                .order_by('-visits')
                .values_list('product', flat=True)[:10]
            )
            popular_products = Product.objects.filter(id__in=pop_prod_ids) if pop_prod_ids else Product.objects.order_by('?')[:10]

        # Optional: GIF
        gif = SearchGif.objects.first()
        gif_url = gif.image.url if gif else None

        data = {
            "gif": gif_url,
            "suggested_categories": CategoryNameSerializer(suggested_categories, many=True).data,
            "popular_categories": CategoryNameSerializer(popular_categories, many=True).data,
            # 👇 Suggested products with extra fields
            "suggested_products": SuggestedProductSerializer(suggested_products, many=True).data,
            # 👇 Popular products untouched
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


# class CategoryProductImagesAPIView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         cloud_name = "dvllntzo0"  # ⚠️ Replace this with your actual Cloudinary cloud name
#         all_images = []
#         image_id_counter = 1

#         categories = Category.objects.all()

#         category_data = []

#         for category in categories:
#             # ✅ Add category image to "All"
#             if category.image:
#                 all_images.append({
#                     "id": image_id_counter,
#                     "url": f"https://res.cloudinary.com/{cloud_name}/image/upload/{category.image.public_id}"
#                 })
#                 image_id_counter += 1

#             # ✅ Collect first image from each product in the category
#             product_images = []
#             products = Product.objects.filter(category=category)

#             for product in products:
#                 if isinstance(product.images, list) and product.images:
#                     for img in product.images:
#                         product_images.append({
#                             "id": product.id,
#                             "url": img
#                         })

#             category_data.append({
#                 "name": category.name,
#                 "images": product_images
#             })

#         response_data = [
#             {
#                 "name": "All",
#                 "images": all_images
#             }
#         ] + category_data

#         return Response(response_data) 


# class CategoryProductImagesAPIView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         all_images = []
#         image_id_counter = 1  # Unique ID for each image

#         categories = Category.objects.all()
#         category_data = []

#         for category in categories:
#             products = Product.objects.filter(category=category)
#             product_images = []

#             for product in products:
#                 if isinstance(product.images, list) and product.images:
#                     for img_url in product.images:
#                         image_data = {
#                             "id": image_id_counter,
#                             "url": img_url
#                         }
#                         product_images.append(image_data)
#                         all_images.append(image_data)
#                         image_id_counter += 1  # ✅ Ensure each image has a unique ID

#             category_data.append({
#                 "name": category.name,
#                 "images": product_images
#             })

#         response_data = [
#             {
#                 "name": "All",
#                 "images": all_images
#             }
#         ] + category_data

#         return Response(response_data)


class CategoryProductImagesAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        all_images_dict = {}  # Use dict to avoid duplicate URLs

        categories = Category.objects.all()
        category_data = []

        for category in categories:
            products = Product.objects.filter(category=category)
            product_images = []

            for product in products:
                if isinstance(product.images, list) and product.images:
                    for img_url in product.images:
                        image_data = {
                            "id": product.id,
                            "url": img_url
                        }
                        product_images.append(image_data)
                        all_images_dict[img_url] = image_data  # Add once globally

            category_data.append({
                "name": category.name,
                "images": product_images
            })

        all_images = list(all_images_dict.values())

        response_data = [
            {
                "name": "All",
                "images": all_images
            }
        ] + category_data

        return Response(response_data)

class UncategorizedProductListAPIView(APIView):
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Assuming `category` is a ForeignKey field
        uncategorized_products = Product.objects.filter(category__isnull=True)
        
        # If using ManyToManyField for category:
        # uncategorized_products = Product.objects.filter(category=None)

        serializer = ProductSerializer(uncategorized_products, many=True, context={'request': request})
        return Response(serializer.data)

class ProductCategoryAssignAPIView(APIView):
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound("Product not found.")

        if product.category:
            return Response({"error": "This product already has a category."}, status=400)

        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        category_id = request.data.get("category_id")

        if not category_id:
            return Response({"error": "'category_id' is required."}, status=400)

        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound("Product not found.")

        if product.category:
            return Response({"error": "Product already has a category."}, status=400)

        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise NotFound("Category not found.")

        product.category = category
        product.save()

        serializer = ProductSerializer(product, context={'request': request})
        return Response({
            "message": "Category assigned successfully.",
            "product": serializer.data
        })


class ModelCountsAPIView(APIView):
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "product_count": Product.objects.count(),
            "category_count": Category.objects.count(),
            "product_enquiry_count": ProductEnquiry.objects.count(),
            "user_count": Register.objects.count(),
        }
        return Response(data)




class GlobalSearchAPIView(APIView):
    authentication_classes = [CombinedJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get('q', '').strip()

        if not query:
            return Response({"detail": "Please provide a search query."}, status=400)

        # Products
        product_results = Product.objects.filter(
            Q(head__icontains=query) | Q(description__icontains=query)
        )
        product_data = ProductSerializer(product_results, many=True).data

        # Categories
        category_results = Category.objects.filter(name__icontains=query)
        category_data = CategorySerializer(category_results, many=True).data

        # Product Enquiries
        enquiry_results = ProductEnquiry.objects.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query) |
            Q(message__icontains=query)
        )
        enquiry_data = ProductEnquirySerializer(enquiry_results, many=True).data

        # Users
        user_results = Register.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(name__icontains=query)
        )
        user_data = RegisterSerializer(user_results, many=True).data

        # ✅ Occasions
        occasion_results = Occasion.objects.filter(name__icontains=query)
        occasion_data = OccasionSerializer(occasion_results, many=True).data

        return Response({
            "products": product_data,
            "categories": category_data,
            "enquiries": enquiry_data,
            "users": user_data,
            "occasions": occasion_data  # ✅ Add to response
        })




