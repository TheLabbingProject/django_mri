from django.contrib import admin
from django_analyses.models.analysis import Analysis
from django_analyses.models.analysis_version import AnalysisVersion
from django_analyses.models.input.definitions.input_definition import InputDefinition
from django_analyses.models.input.input import Input
from django_analyses.models.input.input_specification import InputSpecification
from django_analyses.models.output.definitions.output_definition import OutputDefinition
from django_analyses.models.output.output import Output
from django_analyses.models.output.output_specification import OutputSpecification
from django_analyses.models.run import Run


class AnalysisVersionInline(admin.TabularInline):
    model = AnalysisVersion


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "created", "modified")
    inlines = [AnalysisVersionInline]


@admin.register(AnalysisVersion)
class AnalysisVersionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("analysis", "title", "description")}),
        (
            "Advanced Options",
            {
                "classes": ("collapse",),
                "fields": ("run_method_key", "nested_results_attribute",),
            },
        ),
    )

    def name(self, instance) -> str:
        return str(instance)


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "analysis_version",
        "created",
    )


@admin.register(Input)
class InputAdmin(admin.ModelAdmin):
    list_display = ("run_id", "key", "value", "analysis_version")
    list_filter = (
        "run__analysis_version",
        "run__id",
    )
    list_display_links = None

    def get_queryset(self, request):
        return super(InputAdmin, self).get_queryset(request).select_subclasses()

    def analysis_version(self, instance) -> str:
        return str(instance.run.analysis_version)

    def run_id(self, instance) -> str:
        return instance.run.id


@admin.register(Output)
class OutputAdmin(admin.ModelAdmin):
    list_display = ("run_id", "key", "value", "analysis_version")
    list_filter = (
        "run__analysis_version",
        "run__id",
    )
    list_display_links = None

    def get_queryset(self, request):
        return super(OutputAdmin, self).get_queryset(request).select_subclasses()

    def run_id(self, instance) -> str:
        return instance.run.id

    def analysis_version(self, instance) -> str:
        return str(instance.run.analysis_version)


@admin.register(InputDefinition)
class InputDefinitionAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "description",
        "min_value",
        "max_value",
        "default",
        "choices",
        "required",
        "is_configuration",
    )
    list_filter = ("inputspecification__analysis__title", "inputspecification__id")

    def get_queryset(self, request):
        return (
            super(InputDefinitionAdmin, self).get_queryset(request).select_subclasses()
        )

    def choices(self, instance) -> list:
        return instance.choices if hasattr(instance, "choices") else []

    def min_value(self, instance):
        return instance.min_value if hasattr(instance, "min_value") else None

    def max_value(self, instance):
        return instance.max_value if hasattr(instance, "max_value") else None


@admin.register(OutputDefinition)
class OutputDefinition(admin.ModelAdmin):
    list_display = ("key", "description", "analysis")
    list_filter = ("outputspecification__analysis__title", "outputspecification__id")

    def analysis(self, instance):
        return instance.outputspecification_set.first().analysis


class InputDefinitionsInline(admin.TabularInline):
    model = InputDefinition.inputspecification_set.through
    verbose_name_plural = "Input Definitions"


@admin.register(InputSpecification)
class InputSpecificationAdmin(admin.ModelAdmin):
    fields = ("analysis",)
    list_display = ("id", "analysis")
    list_filter = ("analysis",)
    inlines = [InputDefinitionsInline]


@admin.register(OutputSpecification)
class OutputSpecificationAdmin(admin.ModelAdmin):
    fields = ("analysis",)
    list_display = ("id", "analysis")
    list_filter = ("analysis",)

