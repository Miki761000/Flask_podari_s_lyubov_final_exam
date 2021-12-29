
from resources.admin import CreateAdmin
from resources.auth import Register, Login
from resources.categories import (
    CategoriesGetAllResource,
    CategoriesCreateResource,
    CategoriesEditResource,
    CategoriesDeleteResource,
    CategoriesDetailResource
)
from resources.products import (
    ProductsGetAllResource,
    ProductsCreateResource,
    ProductsEditResource,
    ProductsDeleteResource,
    ProductsDetailResource,
    AddDecreaseQuantity,
)

routes = (
    (Register, "/register"),
    (Login, "/login"),
    (CreateAdmin, "/admins/create-admin/<int:id_>"),
    (CategoriesGetAllResource, "/category"),
    (CategoriesCreateResource, "/category/create"),
    (CategoriesEditResource, "/category/edit/<int:id_>"),
    (CategoriesDeleteResource, "/category/delete/<int:id_>"),
    (CategoriesDetailResource, "/category/detail/<int:id_>"),
    (ProductsGetAllResource, "/products"),
    (ProductsCreateResource, "/products/create"),
    (ProductsEditResource, "/products/edit/<int:id_>"),
    (ProductsDeleteResource, "/products/delete/<int:id_>"),
    (ProductsDetailResource, "/products/detail/<int:id_>"),
    (AddDecreaseQuantity, "/products/edit-quantity/<int:id_>"),
)
