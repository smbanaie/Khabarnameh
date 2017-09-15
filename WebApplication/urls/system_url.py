from itertools import permutations
from WebApplication.handlers.system import dashboard, roles, collections, permissions, user_roles_management, news, \
    users_management, suggestions, messages,consultation, subsystem_management, forums, comments, support, settings
from WebApplication.handlers.system.poll import *
from WebApplication.handlers.system.active_email import ActiveEmailHandler

system_urls = [

    (r'^(?i)/System/Dashboard[/]?$', dashboard.SystemDashboardHandler),
    (r'/System/Dashboard', dashboard.SystemDashboardHandler, None, 'system_dashboard'),

    (r'^(?i)/System/Roles[/]?$', roles.SystemRolesHandler),
    (r'/System/Roles', roles.SystemRolesHandler, None, 'system_roles'),

    (r'^(?i)/System/Collections[/]?$', collections.SystemCollectionsHandler),
    (r'/System/Collections', collections.SystemCollectionsHandler, None, 'system_collections'),

    (r'^(?i)/System/Collections/Action/([\w+^/]+)/([\d+^/]+)?[/]?$', collections.SystemCollectionsActionHandler),
    (r'/System/Collections/Action/(Add|Edit|Delete|ShowUsers)/(id)', collections.SystemCollectionsActionHandler, None,
     'system_collections_action'),

    (r'^(?i)/System/Roles/AccessCollection[/]?$', roles.SystemCollectionRolesHandler),
    (r'/System/Roles/AccessDefaultCollection', roles.SystemCollectionRolesHandler, None, 'system_collections_roles'),

    (r'^(?i)/System/Roles/DefaultCollection[/]?$', roles.SystemDefaultCollectionRolesHandler),
    (r'/System/Roles/DefaultCollection', roles.SystemDefaultCollectionRolesHandler, None,
     'system_default_collections_roles'),

    (r'^(?i)/System/Permissions[/]?$', permissions.SystemPermissionsHandler),
    (r'/System/Permissions', permissions.SystemPermissionsHandler, None, 'system_permissions'),

    (r'^(?i)/System/UserRolesManagement/Roles[/]?$', user_roles_management.SystemUserRolesManagementHandler),
    (r'/System/UserRolesManagement/Roles', user_roles_management.SystemUserRolesManagementHandler, None,
     'system_user_management_roles'),

    (r'^(?i)/System/UserRolesManagement/AddEditors[/]?$', user_roles_management.SystemURmEditorManagementHandler),
    (r'/System/UserRolesManagement/AddEditors', user_roles_management.SystemURmEditorManagementHandler, None,
     'system_urm_editors'),

    (r'^(?i)/System/News/Add[/]?$', news.SystemAddNewsHandler),
    (r'/System/News/Add', news.SystemAddNewsHandler, None, 'system_add_news'),

    (r'^(?i)/System/News/Management[/]?([\d+]+)?[/]?([\w+]+)?[/]?([\w+]+)?[/]?$', news.SystemNewsManagementHandler),
    (r'/System/News/Management', news.SystemNewsManagementHandler, None, 'system_news_management'),
    (r'/System/News/Management/(id)/(coll_id)/(sub_id)', news.SystemNewsManagementHandler, None,
     'system_news_management_pagination'),
    ("/GetCollections", news.GetCollectionsHandler, None, "get_collections"),

    (r'^(?i)/System/News/Edit/([\d+^/]+)[/]?$', news.SystemNewsEditHandler),
    (r'/System/News/Edit/(id)', news.SystemNewsEditHandler, None, 'system_news_edit'),

    (r'^(?i)/System/News/PendingNews[/]?([\d+^/]+)?[/]?$', news.SystemPendingNewsHandler),
    (r'/System/News/PendingNews', news.SystemPendingNewsHandler, None, 'system_news_waiting'),
    (r'/System/News/PendingNews/(id)', news.SystemPendingNewsHandler, None, 'system_news_waiting_by_id'),

    (r'^(?i)/System/UsersManagement/AddUsers[/]?$', users_management.SystemUmAddUsersHandler),
    (r'/System/UsersManagement/AddUsers', users_management.SystemUmAddUsersHandler, None, 'system_um_add_users'),

    (r'^(?i)/System/UsersManagement/Users/([\w:_,+^/]+)?[/]?$', users_management.SystemUmAUsersListHandler),
    (r'/System/UsersManagement/Users', users_management.SystemUmAUsersListHandler, None, 'system_um_users_list'),
    ("/GetRoles", users_management.GetRolsHandler, None, "get_roles"),

    (r'^(?i)/System/ManageUserGuest[/]?$', users_management.SystemManageUserGuestHandler),
    (r'/System/ManageUserGuest', users_management.SystemManageUserGuestHandler, None, 'system_manage_user_guest'),

    (r'^(?i)/System/Help[/]?([\d+^/]+)?[/]?$', dashboard.SystemHelpHandler),
    (r'/System/Help', dashboard.SystemHelpHandler, None, 'system_help'),
    (r'/System/Help/(id)', dashboard.SystemHelpHandler, None, 'system_help_by_id'),

    (r'^(?i)/System/Suggestions[/]?$', suggestions.SuggestionsHandler),
    (r'/System/Suggestions', suggestions.SuggestionsHandler, None, 'system_suggestions'),

    (r'^(?i)/System/Messages/SendNew[/]?$', messages.SendMessagesHandler),
    (r'/System/Messages/SendNew', messages.SendMessagesHandler, None, 'system_messages_send_new'),

    (r'^(?i)/System/Messages/Received[/]?$', messages.ReceivedMessagesHandler),
    (r'/System/Messages/Received', messages.ReceivedMessagesHandler, None, 'system_messages_received'),

    (r'^(?i)/System/Messages/Sent[/]?$', messages.SentMessagesHandler),
    (r'/System/Messages/Sent', messages.SentMessagesHandler, None, 'system_messages_sent'),


    # (r'^(?i)/System/Consultation/SendNew[/]?$', consultation.SendConsultationHandler),
    # (r'/System/Consultation/SendNew', consultation.SendConsultationHandler, None, 'system_consultation_send_new'),

    (r'^(?i)/System/Consultation/Received[/]?$', consultation.ReceivedConsultationHandler),
    (r'/System/Consultation/Received', consultation.ReceivedConsultationHandler, None, 'system_consultation_received'),

    # (r'^(?i)/System/Consultation/Sent[/]?$', consultation.SentConsultationHandler),
    # (r'/System/Consultation/Sent', consultation.SentConsultationHandler, None, 'system_consultation_sent'),



    (r'^(?i)/System/Comments[/]?$', comments.ShowCommentsHandler),
    (r'/System/Comments', comments.ShowCommentsHandler, None, 'system_comments'),

    (r'/System/ActiveEmail/([\d+^/]+)[/]?$', ActiveEmailHandler),
    (r'/System/ActiveEmail/(id)', ActiveEmailHandler, None, 'system_active'),

    (r'/System/Poll/Insert', PollInsertHandler, None, 'system_poll_insert'),
    (r'/System/Poll/Result', PollResultHandler, None, 'system_poll_result'),

    (r'^(?i)/System/Support/SendNewTicket[/]?$', support.SendNewTicketHandler),
    (r'/System/Support/SendNewTicket', support.SendNewTicketHandler, None, 'system_support_send_new_ticket'),

    (r'^(?i)/System/Support/MyTickets[/]?$', support.MyTicketsHandler),
    (r'/System/Support/MyTickets', support.MyTicketsHandler, None, 'system_support_my_tickets'),

    (r'^(?i)/System/Support/MyTickets/Show/([\d+^/]+)[/]?$', support.MyTicketsShowHandler),
    (r'/System/Support/MyTickets/Show/(id)', support.MyTicketsShowHandler, None,
     'system_support_my_tickets_show_by_id'),

    (r'^(?i)/System/Create/SubSystem[/]?$', subsystem_management.InsertSubSystemHandler),
    (r'/System/Create/SubSystem', subsystem_management.InsertSubSystemHandler, None, 'system_insert_subsystem'),

    (r'^(?i)/System/Show/SubSystems[/]?$', subsystem_management.ShowSubSystemsHandler),
    (r'/System/Show/SubSystems', subsystem_management.ShowSubSystemsHandler, None, 'system_show_subsystems'),

    (r'^(?i)/System/Edit/SubSystem/([\d+^/]+)[/]?$', subsystem_management.EditOneSubSystemHandler),
    (r'/System/Edit/SubSystem/(id)', subsystem_management.EditOneSubSystemHandler, None, 'system_edit_one_subsystem'),

    (r'^(?i)/System/Settings/SubDomain[/]?$', settings.SystemSettingsSubDomainHandler),
    (r'/System/Settings/SubDomain', settings.SystemSettingsSubDomainHandler, None, 'system_settings_subdomain'),

    (r'^(?i)/System/Settings/Notification[/]?$', settings.SystemSettingsNotificationHandler),
    (
        r'/System/Settings/Notification', settings.SystemSettingsNotificationHandler, None,
        'system_settings_notification'),

    (r'^(?i)/System/Forum/Topics/Show[/]?$', forums.SystemShowTopicsHandler),
    (r'/System/Forum/Topics/Show', forums.SystemShowTopicsHandler, None, 'system_show_topics'),

    (r'^(?i)/System/Forum/Topic/Posts/Show/([\d+^/]+)[/]?$', forums.SystemForumTopicPostHandler),
    (r'/System/Forum/Topic/Posts/Show/(id)', forums.SystemForumTopicPostHandler, None, 'system_forum_topic_show_post'),

    (r'^(?i)/System/Forum/PendingPosts[/]?$', forums.SystemForumPendingPostsHandler),
    (r'/System/Forum/PendingPosts', forums.SystemForumPendingPostsHandler, None, 'system_forum_pending_posts'),

]
