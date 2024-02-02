# Simple utility class which provides an access to Fortnite service status report.
# Usage: ForniteStatus().getStatus()

import requests as req
import html5lib
from bs4 import BeautifulSoup

class FortniteStatus:
    """
    Instantiate a FortniteStatus class.
    """

    class Status:
        serviceStatuses = []

        def prettify(self):
            return 'Fortnite services status:\n' + '\n'.join([serviceStatus.prettify() for serviceStatus in self.serviceStatuses])

    class ServiceStatus:
        serviceName = ''
        status = False

        def __init__(self, serviceName, status):
            self.serviceName = serviceName
            self.status = status

        def prettify(self):
            return f'{self.serviceName}, {self.status}'

    def __findFortniteStatusHtmlComponent(self, html):
        for component in html.findAll('div', {'class': 'component-container'}):
                innerContainers = component.findAll('div', {'class': 'component-inner-container'})
                for innerContainer in innerContainers:
                    for names in innerContainer.findAll('span', {'class': 'name'}):
                        for name in names.findAll('span'):
                            if 'class' not in name.attrs and 'Fortnite' in name.text:
                                return component

    def __parseFortniteStatus(self, html):
        component = self.__findFortniteStatusHtmlComponent(html)
        status = self.Status()
        childContainer = component.find('div', {'class': 'child-components-container'})
        for innerContainer in childContainer.findAll('div', {'class': 'component-inner-container'}):
            name = innerContainer.find('span', {'class': 'name'}).text.strip()
            statusString = innerContainer.find('span', {'class': 'component-status'}).text.strip()
            if statusString == 'Operational':
                statusCode = True
            else:
                statusCode = False
            status.serviceStatuses.append(self.ServiceStatus(name, statusCode))

        return status

    def getStatus(self):
        webContent = req.get("https://status.epicgames.com/")
        parsedHtml = BeautifulSoup(webContent.text, 'html5lib')

        return self.__parseFortniteStatus(parsedHtml)



    def printStatus(self):
        """
        Prints a current Fortnite services status in stdout.
        Example:

        """
        print(self.generateFortniteStatusReport())

# Example call
fortniteStatus = FortniteStatus()
print(fortniteStatus.getStatus().prettify())