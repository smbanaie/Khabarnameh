from WebApplication.handlers import main, auth, plans

main_urls = [
    (r'/', main.IndexHandler, None, 'index'),

    # (r'^(?i)/([\d+^/]+)(-[^/]*)?[/]?$', auth.LoginHandler),
    # (r'^(?i)/([\d+^/]+)(-[^/]*)?/Login[/]?$', auth.LoginHandler),
    # (r'^/(system_id)-(system_name)/Login$', auth.LoginHandler, None, 'login'),

    (r'^(?i)/Login[/]?$', auth.LoginHandler),
    (r'^/Login$', auth.LoginHandler, None, 'login'),

    (r'^(?i)/Logout[/]?$', auth.LogoutHandler),
    (r'^/Logout$', auth.LogoutHandler, None, 'logout'),

    (r'^(?i)/([\d+]+)?[/]?AppDownload[/]?$', main.DownloadAppHandler),
    (r'^/(system_id)/AppDownload', main.DownloadAppHandler, None, 'download_app'),
    (r'^/AppDownload', main.DownloadAppHandler, None, 'download_public_app'),

    ("/GetCities", auth.GetCitiesHandler, None, "get_cities"),

    (r'^(?i)/Plans/([\d+^/]+)/Orders[/]?([^/]?Step1|[^/]?Step2|[^/]?Step3)?[/]?', plans.PlansHandler),
    (r'^/Plans/(id)/Orders', plans.PlansHandler, None, 'plans_order'),
    (r'^/Plans/(id)/Orders/(Step1|Step2|Step3)', plans.PlansHandler , None, 'plans_order_by_step'),

    # (r'^(?i)/Signup/1-Start[/]?$', auth.SignupHandler),
    # (r'^/Signup/1-Start$', auth.SignupHandler, None, 'signup'),



]