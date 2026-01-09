import time
import threading
from jnius import autoclass
from config import ConfigManager

def get_foreground_app():
    """
    Returns the package name of the current foreground app.
    Requires PACKAGE_USAGE_STATS permission.
    """
    try:
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Context = autoclass('android.content.Context')
        UsageStatsManager = autoclass('android.app.usage.UsageStatsManager')
        System = autoclass('java.lang.System')
        
        context = PythonActivity.mActivity if PythonActivity.mActivity else autoclass('org.kivy.android.PythonService').mService
        usm = context.getSystemService(Context.USAGE_STATS_SERVICE)
        
        now = System.currentTimeMillis()
        # Check last 10 seconds
        stats = usm.queryUsageStats(UsageStatsManager.INTERVAL_DAILY, now - 1000 * 10, now)
        
        if stats and stats.size() > 0:
            stats = stats.toArray()
            # Sort by last time used
            # We need to manually iterate to find the most recent
            recent_stat = None
            max_time = 0
            
            for i in range(len(stats)):
                stat = stats[i]
                if stat.getLastTimeUsed() > max_time:
                    max_time = stat.getLastTimeUsed()
                    recent_stat = stat
            
            if recent_stat:
                return recent_stat.getPackageName()
                
    except Exception as e:
        print(f"Error getting foreground app: {e}")
        
    return None

def block_screen(context):
    """
    Launches the block screen activity or overlay.
    For simplicity, we bring our app to front.
    """
    try:
        Intent = autoclass('android.content.Intent')
        # We assume the main activity is the standard Kivy one
        # package name is defined in buildozer.spec
        package_name = context.getPackageName()
        
        PackageManager = context.getPackageManager()
        intent = PackageManager.getLaunchIntentForPackage(package_name)
        
        if intent:
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            intent.addFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT)
            context.startActivity(intent)
            
    except Exception as e:
        print(f"Error blocking screen: {e}")

if __name__ == '__main__':
    from jnius import autoclass
    
    # Kivy service setup
    PythonService = autoclass('org.kivy.android.PythonService')
    service = PythonService.mService
    
    config = ConfigManager('service_config.json') # Service might need its own config path or shared
    # Note: Android paths are different. We need absolute path usually.
    # For now assuming same dir works or we set it in main.
    
    # We should get the path from context
    Context = autoclass('android.content.Context')
    files_dir = service.getFilesDir().getAbsolutePath()
    config = ConfigManager(files_dir + '/config.json')
    
    print("Service started")
    
    while True:
        try:
            # Refresh config occasionally
            config.load()
            
            # Check schedule
            # (Simplified check, assuming always enabled for testing logic)
            blocked_apps = config.get_blocked_apps()
            
            if blocked_apps:
                fg_app = get_foreground_app()
                
                if fg_app and fg_app in blocked_apps:
                    print(f"Blocking {fg_app}")
                    # Launch Block UI
                    block_screen(service)
            
            # Sleep 1 second
            time.sleep(1)
            
        except Exception as e:
            print(f"Service loop error: {e}")
            time.sleep(5)
