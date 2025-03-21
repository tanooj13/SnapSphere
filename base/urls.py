from django.urls import path
from . import views 

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('post/',views.post,name='post'),
    path('delete-snap/<int:snap_id>/',views.delete_snap,name='delete-snap'),
    path('update-snap/<int:snap_id>/',views.update_snap,name='update-snap'),
    path('profile/<str:username>/',views.profile_view,name='profile-view'),
    path('profile/',views.profile,name="profile"),
    path('like-snap/<int:snap_id>/',views.like,name='like-snap'),
    path('comment-snap/<int:snap_id>/',views.comment,name='comment-snap'),
    path('delete-comment/<int:snap_id>/<int:comment_id>',views.delete_comment,name='delete-comment'),
    path('edit-comment/<int:snap_id>/<int:comment_id>',views.edit_comment,name='edit-comment'),
    path('save-snap/<int:snap_id>/',views.save_snap,name='save-snap'),
    path('saved-snaps/',views.show_saved,name='saved-snaps'),
    path('delete-acoount/',views.delete_account,name='delete-account'),
    

]