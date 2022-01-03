from resources.admin import CreateAdmin
from resources.auth import Register, Login
from resources.categories import (
    CategoriesCreateResource,
    CategoriesEditResource,
)
from resources.products import (
    ProductsCreateResource,
    ProductsEditResource,
    AddDecreaseQuantity,
)

routes = (
    (Register, "/register"),
    (Login, "/login"),
    (CreateAdmin, "/admins/create-admin/<int:id_>"),
    (CategoriesCreateResource, "/category"),
    (CategoriesEditResource, "/category/<int:id_>"),
    (ProductsCreateResource, "/products"),
    (ProductsEditResource, "/products/<int:id_>"),
    (AddDecreaseQuantity, "/products/edit-quantity/<int:id_>"),
)
