import menus

while True:
    match menus.Default.select():
        case "WebPasswordsView":
            menus.WebPasswordsView.list()
        case "BrowsingVisitsHistoryView":
            menus.BrowsingVisitsHistoryView.getVisits()
        case "BrowsingURLsHistoryView":
            menus.BrowsingURLsHistoryView.getURLs()
        case "PhotoMetadataView":
            menus.PhotoMetadataView.list()
        