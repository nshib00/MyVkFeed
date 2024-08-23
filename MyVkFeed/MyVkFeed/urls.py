urlpatterns = [path("admin/", admin.site.urls), path("", include("main.urls"))]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = main.views.page_not_found
>>>>>>> dev