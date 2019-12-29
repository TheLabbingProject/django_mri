from django.urls import include, path
from django_analyses import views
from rest_framework import routers

app_name = "django_analyses"
router = routers.DefaultRouter()
router.register(r"analysis", views.AnalysisViewSet)
router.register(r"analysis_version", views.AnalysisVersionViewSet)
router.register(r"category", views.CategoryViewSet)
router.register(r"output_specification", views.OutputSpecificationViewSet)
router.register(r"run", views.RunViewSet)
router.register(r"node", views.NodeViewSet)
router.register(r"pipe", views.PipeViewSet)
router.register(r"pipeline", views.PipelineViewSet)

# In viewsets of base models basename must be provided because of the `get_queryset`
# method override. Since the `queryset` attribute is not provided the basename cannot
# be infered.
router.register(r"input", views.InputViewSet, basename="input")
router.register(
    r"input_definition", views.InputDefinitionViewSet, basename="inputdefinition"
)
router.register(r"input_specification", views.InputSpecificationViewSet)
router.register(r"output", views.OutputViewSet, basename="output")
router.register(
    r"output_definition", views.OutputDefinitionViewSet, basename="outputdefinition"
)


urlpatterns = [path("analysis/", include(router.urls))]

