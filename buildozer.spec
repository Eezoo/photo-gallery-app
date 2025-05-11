[app]

# عنوان التطبيق
title = معرض الصور المتقدم

# اسم الحزمة (يجب أن يكون فريداً)
package.name = photogalleryapp

# اسم المجال (يجب أن يكون عكسياً)
package.domain = com.example

# إصدار التطبيق
version = 1.0.0

# وصف التطبيق
description = تطبيق معرض الصور باستخدام Flet

# مصدر التطبيق
source.dir = .

# الملف الرئيسي للتشغيل
source.main = main.py

# المكتبات المطلوبة
requirements = python3,cython==0.29.36,flet,opencv-python,numpy,android

# أذونات Android
android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# الحد الأدنى من إصدار Android SDK
android.minapi = 21

# إصدار Android SDK الهدف
android.targetapi = 34

# نوع الواجهة
android.sdl = 2

[buildozer]

# إعدادات Buildozer
log_level = 2
warn_on_root = 1
