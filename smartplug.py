__author__ = 'rohit'

import requests
from xml.dom.minidom import getDOMImplementation
from xml.dom.minidom import parseString


class SmartPlug(object):
    """
    Simple class to access a "EDIMAX Smart Plug Switch SP-1101W"

    Usage example when used as library:

    p = SmartPlug("172.16.100.75", ('admin', '1234'))

    # change state of plug
    p.state = "OFF"
    p.state = "ON"

    # query and print current state of plug
    print(p.state)

    """

    def __init__(self, host, auth):

        """
        Create a new SmartPlug instance identified by the given URL.

        :rtype : object
        :param host: The IP/hostname of the SmartPlug. E.g. '172.16.100.75'
        :param auth: User and password to authenticate with the plug. E.g. ('admin', '1234')
        """

        self.url = "http://%s:10000/smartplug.cgi" % host
        self.auth = auth
        self.domi = getDOMImplementation()

    def _xml_cmd_setget_state(self, cmdId, cmdStr):

        """
        Create XML representation of a state command.

        :type self: object
        :type cmdId: str
        :type cmdStr: str
        :rtype: str
        :param cmdId: Use 'get' to request plug state, use 'setup' change plug state.
        :param cmdStr: Empty string for 'get', 'ON' or 'OFF' for 'setup'
        :return: XML representation of command
        """
        doc = self.domi.createDocument(None, "SMARTPLUG", None)
        doc.documentElement.setAttribute("id", "edimax")

        cmd = doc.createElement("CMD")
        cmd.setAttribute("id", cmdId)
        state = doc.createElement("Device.System.Power.State")
        cmd.appendChild(state)
        state.appendChild(doc.createTextNode(cmdStr))

        doc.documentElement.appendChild(cmd)

        return doc.toxml()

    def _post_xml(self, xml):

        """
        Post XML command as multipart file to SmartPlug, parse XML response.

        :type self: object
        :type xml: str
        :rtype: str
        :param xml: XML representation of command (as generated by _xml_cmd)
        :return: 'OK' on success, 'FAILED' otherwise
        """

        files = {'file': xml}

        res = requests.post(self.url, auth=self.auth, files=files)

        if res.status_code == requests.codes.ok:
            dom = parseString(res.text)

            try:
                val = dom.getElementsByTagName("CMD")[0].firstChild.nodeValue

                if val is None:
                    val = dom.getElementsByTagName("CMD")[0].getElementsByTagName("Device.System.Power.State")[0].\
                        firstChild.nodeValue

                return val

            except Exception as e:

                print(e.__str__())

        return None

    @property
    def state(self):

        """
        Get the current state of the SmartPlug.

        :type self: object
        :rtype: str
        :return: 'ON' or 'OFF'
        """

        res = self._post_xml(self._xml_cmd_setget_state("get", ""))

        if res != "ON" and res != "OFF":
            raise Exception("Failed to communicate with SmartPlug")

        return res

    @state.setter
    def state(self, value):

        """
        Set the state of the SmartPlug

        :type self: object
        :type value: str
        :param value: 'ON', 'on', 'OFF' or 'off'
        """

        if value == "ON" or value == "on":
            res = self._post_xml(self._xml_cmd_setget_state("setup", "ON"))
        else:
            res = self._post_xml(self._xml_cmd_setget_state("setup", "OFF"))

        if res != "OK":
            raise Exception("Failed to communicate with SmartPlug")

"""
TESTING ONLY
if __name__ == "__main__":

    p = SmartPlug('192.168.1.61', ('admin', '1234'))
    p.state = 'ON'
"""