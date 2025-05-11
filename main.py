import os
import cv2
from datetime import datetime
import flet as ft
from flet import icons


class PhotoGalleryApp:
    """
    فئة تطبيق معرض الصور المتقدم
    تقوم بإنشاء واجهة مستخدم لالتقاط وعرض وإدارة الصور
    """
    
    def __init__(self):
        """تهيئة التطبيق وإعداد المتغيرات الأساسية"""
        self.image_dir = "photos"  # مجلد تخزين الصور
        os.makedirs(self.image_dir, exist_ok=True)  # إنشاء المجلد إذا لم يكن موجوداً
        self.selected_photos = []  # قائمة لتخزين الصور المحددة

    def main(self, page: ft.Page):
        """الدالة الرئيسية لتشغيل التطبيق"""
        self.page = page  # حفظ مرجع الصفحة
        self.setup_page()  # تهيئة إعدادات الصفحة
        self.create_controls()  # إنشاء عناصر التحكم
        self.setup_events()  # ربط الأحداث بالوظائف
        self.load_photos()  # تحميل الصور الموجودة
        #self.page.add(self.build_ui())  # بناء واجهة المستخدم    
        self.current_page = 1  # الصفحة الحالية (1 أو 2)
        self.show_page1()  # عرض الواجهة الأولى عند البدء     
        self.page.update()# تحديث الصفحة
        
    def setup_page(self):
        """تهيئة إعدادات صفحة التطبيق"""
        self.page.title = "معرض الصور المتقدم"
        self.page.window.left=1140
        self.page.window.top=40
        self.page.window.width = 380  # عرض النافذة
        self.page.window.height = 800  # ارتفاع النافذة
        self.page.theme_mode = ft.ThemeMode.LIGHT  # وضع السمة الفاتحة
        self.page.padding = 10  # الحشو الداخلي
        self.page.window.resizable = True  # قابلية تغيير حجم النافذة
        self.page.bgcolor = 'black'  # لون الخلفية
        self.page.fonts = {"arabic": "assets/NotoNaskhArabic-Regular.ttf"}  # إعداد الخط العربي
        self.page.theme = ft.Theme(font_family="arabic")  # تطبيق الخط العربي
       

    def create_controls(self):
        """إنشاء عناصر التحكم في الواجهة"""
        
            # حقل البحث
        self.search_field = ft.TextField(
            label="بحث عن الصور",
            hint_text="",
            width=250,
            height=40,
            border_radius=25,
            text_size=14,
            bgcolor='white',
            prefix_icon=icons.SEARCH,
            on_change=self.search_photos,
            border_color="white"
            )
        
          # زر الانتقال للصفحة 2
        self.get_in = ft.IconButton(
            width=40,
            height=40,           
            bgcolor='white',  
            icon=icons.ARROW_FORWARD_SHARP,        
            #icon=icons.DOUBLE_ARROW_SHARP,
            icon_color=ft.colors.BLACK87, 
           #on_click=lambda e: self.show_page2() 
                  
        )
            # زر العودة للصفحة 1
        self.get_out = ft.IconButton(
            width=40,
            height=40,           
            bgcolor='white',          
            icon=icons.ARROW_BACK_SHARP,
            icon_color=ft.colors.BLACK87, 
            #on_click=lambda e: self.show_page1()           
        )

        # حقل إدخال اسم الصورة
        self.photo_name = ft.TextField(
            label="اسم الصورة",
            hint_text="أدخل اسمًا للصورة",
            width=200,
            border_radius=25,
            text_size=14
            )
        
        # زر التقاط الصورة
        self.capture_btn = ft.IconButton(     #ElevatedButton
            icon=icons.CAMERA_ALT_OUTLINED,
            icon_color=ft.colors.BLACK87,
            icon_size=60,
            width=80,
            height=80,
            bgcolor="white",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                padding=10
            )
            )
        
        # أزرار التحكم
        self.delete_btn = ft.IconButton(
            icon=icons.DELETE_OUTLINED,
            icon_color=ft.colors.BLACK87,
            width=60,
            height=40,        
            disabled=True,
            #bgcolor='red'
            )
        
        self.share_btn = ft.IconButton(
            icon=icons.SHARE,
            icon_color=ft.colors.BLACK87,
            width=60,
            height=40, 
            tooltip="مشاركة",
            disabled=True,
            #bgcolor='red'
            )
        
        self.refresh_btn = ft.IconButton(
            icon=icons.REFRESH_OUTLINED,
            icon_color=ft.colors.BLACK87,
            icon_size=30,
            tooltip="تحديث",
            on_click=lambda e: self.load_photos()
            )
        
        # معرض الصور
        self.gallery = ft.GridView(
            expand=True,
            runs_count=3,  # عدد الأعمدة
            spacing=10,  # المسافة بين العناصر
            run_spacing=10,  # المسافة بين الصفوف
            padding=10  # الحشو الداخلي
            )
        
        # شريط الحالة
        self.status_bar = ft.Text(
            value="جاهز",
            size=12,
            color=ft.colors.GREY_600
            )
        #مساحه فاضيه
        self.spice = ft.Text(
            width=110,
            #bgcolor='red',
           
            )
        
    #    container = ft.Container( width=320,height=720,bgcolor='blue',
 #           content=ft.Row([ ]))

        

    def setup_events(self):
        """ربط الأحداث بالوظائف المناسبة"""
        self.capture_btn.on_click = self.capture_photo
        self.delete_btn.on_click = self.delete_photos
        self.share_btn.on_click = self.share_photos
        self.get_in.on_click = lambda e: self.show_page2()
        self.get_out.on_click = lambda e: self.show_page1()

    def capture_photo(self, e):
        """وظيفة التقاط صورة من الكاميرا"""
        name = self.photo_name.value.strip()
        if not name:
            self.show_status("الرجاء إدخال اسم الصورة", ft.colors.RED)
            return

        try:
            # فتح الكاميرا
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                self.show_status("الكاميرا غير متوفرة", ft.colors.RED)
                return

            # التقاط الصورة
            ret, frame = cap.read()
            if not ret:
                self.show_status("فشل في التقاط الصورة", ft.colors.RED)
                return

            # حفظ الصورة
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.jpg"
            filepath = os.path.join(self.image_dir, filename)
            
            cv2.imwrite(filepath, frame)
            self.show_status(f"تم حفظ الصورة: {filename}", ft.colors.GREEN)
            self.load_photos()
            
        except Exception as ex:
            self.show_status(f"خطأ: {str(ex)}", ft.colors.RED)
        finally:
            if 'cap' in locals():
                cap.release()  # إغلاق الكاميرا
            self.photo_name.value = ""
            self.page.update()

    def load_photos(self, search_query=None):
        """تحميل الصور من المجلد وعرضها في المعرض"""
        try:
            self.gallery.controls.clear()  # مسح المعرض الحالي
            photos = []  # قائمة لتخزين أسماء الصور
            
            # قراءة محتويات المجلد
            for f in os.listdir(self.image_dir):
                if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                    if search_query and search_query.lower() not in f.lower():
                        continue  # تخطي الصور التي لا تطابق بحث
                    photos.append(f)
            
            # ترتيب الصور حسب تاريخ التعديل (الأحدث أولاً)
            photos.sort(key=lambda x: os.path.getmtime(os.path.join(self.image_dir, x)), reverse=True)
            
            # معرض الصور 
            # إذا لم توجد صور
            if not photos:
                self.gallery.controls.append(
                    ft.Container(bgcolor='red',
                        content=ft.Column([
                            ft.Icon(icons.PHOTO_LIBRARY, size=50, color=ft.colors.GREY_400),
                            ft.Text("لا توجد صور متاحة", size=16, color=ft.colors.GREY)
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                        alignment=ft.alignment.center
                    )
                )
                return
            
            # عرض كل الصور في المعرض
            for photo in photos:
                img_path = os.path.join(self.image_dir, photo)
                
                img_container = ft.Container(
                    content=ft.Column([
                        ft.Image(
                            src=img_path,
                            #width=200,
                            height=45,
                            fit=ft.ImageFit.COVER,
                            border_radius=5,
                            
                        ),
                        ft.Text(
                            photo[:20] + (photo[20:] and '...'),  # تقليل طول اسم الملف إذا كان طويلاً
                            size=10,
                            text_align=ft.TextAlign.CENTER,
                            width="auto"
                        )
                    ], spacing=0),
                    data=img_path,  # تخزين مسار الصورة كبيانات
                    on_click=lambda e: self.toggle_select_photo(e),  # حدث النقر
                    border=ft.border.all(2, ft.colors.TRANSPARENT),  # حد شفاف
                    padding=5,
                    border_radius=10,
                    bgcolor='#d9d9d9',
                    
                )
                
                self.gallery.controls.append(img_container)
            
            self.show_status(f"تم تحميل {len(photos)} صورة", ft.colors.GREEN)
            
        except Exception as ex:
            self.show_status(f"خطأ في تحميل الصور: {str(ex)}", ft.colors.RED)
        finally:
            self.page.update()

    def search_photos(self, e):
        """بحث الصور حسب النص المدخل"""
        self.load_photos(self.search_field.value)

    def toggle_select_photo(self, e):
        """تحديد أو إلغاء تحديد صورة"""
        img_path = e.control.data
        
        if img_path in self.selected_photos:
            # إلغاء التحديد
            self.selected_photos.remove(img_path)
            e.control.border = ft.border.all(2, ft.colors.TRANSPARENT)
        else:
            # تحديد الصورة
            self.selected_photos.append(img_path)
            e.control.border = ft.border.all(2, ft.colors.BLUE_400)
        
        # تفعيل/تعطيل الأزرار حسب وجود صور محددة
        self.delete_btn.disabled = len(self.selected_photos) == 0
        self.share_btn.disabled = len(self.selected_photos) == 0
        
        self.page.update()

    def delete_photos(self, e):
        """حذف الصور المحددة"""
        if not self.selected_photos:
            return
            
        try:
            for photo in self.selected_photos:
                try:
                    os.remove(photo)  # حذف الصورة
                except:
                    continue  # الاستمرار في حالة وجود خطأ
            
            self.show_status(f"تم حذف {len(self.selected_photos)} صورة", ft.colors.GREEN)
            self.selected_photos.clear()  # تفريغ القائمة
            self.delete_btn.disabled = True  # تعطيل زر الحذف
            self.share_btn.disabled = True  # تعطيل زر المشاركة
            self.load_photos()  # إعادة تحميل المعرض
            
        except Exception as ex:
            self.show_status(f"خطأ في الحذف: {str(ex)}", ft.colors.RED)

    def share_photos(self, e):
        """وظيفة مشاركة الصور (مكانية)"""
        if not self.selected_photos:
            return
            
        self.show_status(f"جاهز لمشاركة {len(self.selected_photos)} صورة", ft.colors.BLUE)
        # يمكن إضافة منطق المشاركة هنا (مثل رفع إلى السحابة أو إرسال بالبريد)

    def show_status(self, message, color=None):
        """عرض رسالة في شريط الحالة"""
        self.status_bar.value = message
        if color:
            self.status_bar.color = color
        self.page.update()

##############################################################################################
    def show_page1(self):
            """عرض الصفحة الأولى"""
            self.current_page = 1
            self.page.clean()
            self.page.add(self.build_ui())
            self.page.update()
            
    def show_page2(self):
            """عرض الصفحة الثانية"""
            self.current_page = 2
            self.page.clean()
            self.page.add(self.build_ui2())
            self.page.update()
            
##############################################################################################
    def build_ui(self):
        """بناء واجهة المستخدم"""

        return ft.Container(
    content=ft.Column(        
        controls=[
            # صف البحث والتحديث
            ft.Row([
                self.search_field,
                self.get_in,
                #self.refresh_btn
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Divider(height=500,color="#d9d9d9"),
            
            # صف إدخال الاسم والالتقاط
            ft.Row([
                #self.photo_name,
                self.capture_btn,
                
            ], alignment=ft.MainAxisAlignment.CENTER,),
            
            # صف أزرار التحكم
            #ft.Row([
            #    self.delete_btn,
             #   self.share_btn
            #], alignment=ft.MainAxisAlignment.CENTER),
            
            #ft.Divider(height=20),
            
            # معرض الصور
            #ft.Container(
                #bgcolor='red',
                #content=self.gallery,
                #border=ft.border.all(1, ft.colors.GREY_300),
                #border_radius=10,
                #expand=True,
                #bgcolor='white'
            #),
            
            #ft.Divider(height=10),
            
            # شريط الحالة
            #self.status_bar
        ],
        expand=True,
        spacing=10
    ),
    # يمكنك إضافة خصائص إضافية للـ Container الرئيسي هنا
    padding=25,  # مثال: إضافة padding حول المحتوى
    bgcolor='#d9d9d9',  # مثال: لون الخلفية
    border_radius=25, # مثال: زوايا مدورة
    width=340,
    height=720,

)

    def build_ui2(self):
        """بناء واجهة المستخدم الثانية"""

        return ft.Container(
            content=ft.Column(        
                controls=[
            # صف البحث والتحديث
            ft.Row([
                #self.search_field,
                self.get_out,
                ft.Container(
                    bgcolor="white",
                    width=250,
                    height=40,
                    
                    border_radius=20,
                        content=ft.Row([
                            self.delete_btn,
                            self.spice,
                            self.share_btn,
                            
                    ])
                    ),
            ], alignment=ft.MainAxisAlignment.CENTER),
        
            
            # صف إدخال الاسم والالتقاط
            #ft.Row([
                
                
                #self.photo_name,
                
                
                
            #], alignment=ft.MainAxisAlignment.CENTER,),
            
            # صف أزرار التحكم
            #ft.Row([
            #    
            #], alignment=ft.MainAxisAlignment.CENTER),
            
            #ft.Divider(height=20),
            
            # معرض الصور
            ft.Container(
                content=self.gallery,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=15,
                expand=True,
                bgcolor='white',
                width=320,
            ),
            
            #ft.Divider(height=10),
            
            # شريط الحالة
            #self.status_bar
        ],
        expand=True,
        spacing=10
    ),
    # يمكنك إضافة خصائص إضافية للـ Container الرئيسي هنا
    padding=20,  # مثال: إضافة padding حول المحتوى
    bgcolor='#d9d9d9',  # مثال: لون الخلفية
    border_radius=25, # مثال: زوايا مدورة
    width=340,
    height=720,
    )

if __name__ == "__main__":
    ft.app(target=PhotoGalleryApp().main, view=ft.AppView.FLET_APP)
