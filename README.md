# [SLCB] SendSounds

## Introduction:

This is a Streamlabs Chatbot script mabe by request, created to play sound files to an overlay, simulating a "faux-virtual audio channel" to be added and controlled on OBS, making it possible to sed those files sent to a specific track.

## Features:

- [x] Graphical overlay to control the scripts and sounds settings
- [x] Uses sqlite database instead of json files for storing sounds information
- [x] Uses bot commands provided with the script
- [x] Sends and optional chat message on stream
- [x] Creation of log files for both **StremlabsSystem** script and the **GUI** (aka Dashboard), organized into specific folders
- [x] "Automatic commands" created when adding new files to the sounds folder and "Saving the settings for the script"
- [x] General Overlay volume control, via the script settings
- [x] Individual sounds volume control, so the user can fix each sound level indivudally
- [x] Possibility to check and fix database issues to prevent the script from stop excecuting if an unexistent file requested to be played
  - By disabling entries on the database
  - By deleting entries from the database
  - By deleting entries which sound files were not found in the defined sounds folder
- [x] Possibility to run the GUI in stand alone mode, by using the command prompt
- [x] Possibility to preview the sound effect volume[^1]
- [x] Compatible with the following streaming platforms:
  - Twitch (100%)

## Requirements:

- Windows 10 or above
- Streamlabs Chatbot 1.0.79 or above
- OBS Studio 29.1.3 or above
- Python packages/dependencies[^2]:
  - **pygame 2.0.3** (optional)

## User guide:

A full guide on how to use the script can be found [this wiki](https://github.com/vonschappler/SLCB-SendSounds/wiki).

## Image previews:

<details>
<summary>

### 1. Streamlabs Chatbot GUI:

</summary>

![Image 01 - Interface Streamlabs Chatbot](images/Preview_SLCB.png)
</details>

<details>
<summary>

### 2. Dashboard made with Tkinter:

</summary>

![Image 02 - Preview Dashboard](images/Preview_Dash.png)
</details>

## Changelog:

- [Version 1.0.0](#):
  - First version launched

## Additional information:

<details open>
<summary>

### Issues:

</summary>

  <details open>
  <summary>
  
  #### To Fix:
  </summary>
  
   - [ ] GUI start / update progress may be slow if too many files are added in the database
  </details>

  <details open>
  <summary>
  
  #### Under investigation:
  </summary>
  
   - [x] Overlay may play "broken sounds"
     - Sometimes, when using the command to reload the script with the new information added via the dashboard, may cause OBS to not load the sounds correctly. When / if this happens it's advised to refresh the overlay added to OBS.
     - The cause of this is being ivestigated and if it's found that the issue is caused by the script it self, a fix for it will be released in future patches.
  </details>

  
</details>

<details open>
<summary>

### TODOS:

</summary>

- [ ] Find a way to make the database run smoothly when too many files / entries are added to it
- [ ] Add an option to delete and entry from the database while previnting it to be readded when saving settings
   <details>
  
    - For the moment, entries can only be disabled and previous tests so far, keep re-adding the deleted information with default values whenever the script settings are saved
  </details>
</details>

[^1]: Optional python package **pygame 2.0.3** needs to be installed for this to work
[^2]: Please refer the complete user guide on how to proceed with the instalation of packages/dependencies on **Python 2.7.13**
