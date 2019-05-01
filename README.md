# django-dicom



A django app to manage MRI data.



Quick start
-----------

1. Add "django_smb" to your INSTALLED_APPS setting:

<pre>
    INSTALLED_APPS = [  
        ...  
        'django_dicom',  
    ]  
</pre>

2. Include the dicom URLconf in your project urls.py:

<pre>
    path('mri/', include('django_mri.urls')),
</pre>

3. Run `python manage.py migrate` to create the dicom models.

4. Start the development server and visit http://127.0.0.1:8000/admin/.

5. Visit http://127.0.0.1:8000/mri/.




[1]: https://www.dicomstandard.org/
