from jnius import autoclass
from android.permissions import request_permissions, Permission
from kivy.utils import platform

def check_usage_stats_permission():
    if platform != 'android':
        return True
    
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Context = autoclass('android.content.Context')
    AppOpsManager = autoclass('android.app.AppOpsManager')
    Process = autoclass('android.os.Process')
    
    activity = PythonActivity.mActivity
    app_ops = activity.getSystemService(Context.APP_OPS_SERVICE)
    
    mode = app_ops.checkOpNoThrow(
        AppOpsManager.OPSTR_GET_USAGE_STATS, 
        Process.myUid(), 
        activity.getPackageName()
    )
    
    return mode == AppOpsManager.MODE_ALLOWED

def request_usage_stats_permission():
    if platform != 'android':
        return
        
    from jnius import cast
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Settings = autoclass('android.provider.Settings')
    Uri = autoclass('android.net.Uri')
    
    activity = PythonActivity.mActivity
    intent = Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS)
    activity.startActivity(intent)

def check_overlay_permission():
    if platform != 'android':
        return True
    
    Settings = autoclass('android.provider.Settings')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity
    
    return Settings.canDrawOverlays(activity)

def request_overlay_permission():
    if platform != 'android':
        return
    
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    Settings = autoclass('android.provider.Settings')
    Uri = autoclass('android.net.Uri')
    
    activity = PythonActivity.mActivity
    intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION, 
                    Uri.parse("package:" + activity.getPackageName()))
    activity.startActivity(intent)

def request_standard_permissions():
    if platform == 'android':
        request_permissions([Permission.FOREGROUND_SERVICE, Permission.WAKE_LOCK])
