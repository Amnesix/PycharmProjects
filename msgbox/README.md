# MsgBox

This application allows you to display a dialog box with a random number of buttons
by providing in return the number of the selected button.
It is possible to add a timeout for an automatic closing of the window.

| short | long |Explanation
|:--- |:---- |:----
| -t "title" | --title "title" | Title of dialog
| -m "Message" | --message "Message" | Message of dialog box
| -b "buttons" | --buttons "buttons" | List of buttons label using ';' for separation
| | --timeout N | Timeout in seconds
| | --icon | Name of internal icon (see below) or of gtk icon, or image file name

There are 5 internal images which can be used directly :\
4 gtk icon from Adwaita theme : 'question', 'information', 'warning', 'error' 
and a hourglass gif from [this site](https://www.gifsanimes.com/cat-sabliers-1261.htm)

