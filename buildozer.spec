[app]

# اسم التطبيق
title = معرض الصور المتقدم

# اسم الحزمة (يجب أن يكون فريدًا)
package.name = photogalleryapp

# اسم المجال (يجب أن يكون عكسيًا، مثل com.example)
package.domain = com.example

# إصدار التطبيق
version = 1.0.0

# وصف التطبيق
description = تطبيق معرض الصور باستخدام Flet

# مصدر التطبيق (main.py هو نقطة الدخول)
source.dir = .

# الملف الرئيسي للتشغيل
source.include_exts = py,png,jpg,jpeg,ttf

# المكتبات المطلوبة
requirements = flet,opencv-python,numpy,android

# أذونات Android
android.permissions = CAMERA, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# نسخة Android SDK الأدنى
android.minapi = 21

# نسخة Android SDK الهدف
android.targetapi = 34

# نوع الواجهة (هنا نستخدم SDL2 لأن Flet تعتمد عليها)
android.sdl = 2

# نظام التشغيل الهدف (android)
osx.python_version = 3
osx.arch = x86_64
