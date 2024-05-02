# MultiCam Auto Render Pro

## Description

**MultiCam Auto Render Pro** is a Blender addon designed to simplify the process of rendering scenes from multiple cameras. It allows Blender users to automatically render from each camera in a scene with a user-specified filename and directory, providing real-time progress updates and the ability to cancel rendering mid-process. This tool is ideal for projects requiring multiple angle captures without interrupting workflow.

## Installation

1. **Download the Addon:**
   - Download `multicam_auto_render_pro.py` from the GitHub repository.

2. **Install in Blender:**
   - Open Blender and navigate to `Edit > Preferences > Add-ons`.
   - Click `Install` and select the downloaded `multicam_auto_render_pro.py` file.
   - Enable the addon by ticking the checkbox next to its name.

## Usage

1. **Access the Panel:**
   - Go to the 3D Viewport.
   - Open the sidebar (press `N` if not visible).
   - Navigate to the 'Mahersdesigns' tab.

2. **Set Parameters:**
   - **Render Path:** Set the directory where the renders should be saved.
   - **Base Filename:** Set the base name for the files. Each render will append a number to this base.

3. **Start Rendering:**
   - Click the `Render From Each Camera` button to start the rendering process.
   - The progress will be displayed, showing which camera is currently rendering and the percentage completed.

4. **Cancel Rendering:**
   - If needed, you can stop the rendering process at any time by clicking the `Cancel Rendering` button.

## Features

- Renders from each camera in the scene sequentially.
- User can specify the output directory and filename.
- Real-time progress updates in the Blender UI.
- Ability to cancel the rendering process at any moment.

## Troubleshooting and Common Issues

- **Addon Does Not Appear in Blender:**
  - Ensure that Blender is restarted after installation.
  - Verify that the addon is enabled in the Preferences menu.

- **Rendering Does Not Start:**
  - Check that the specified directory exists and Blender has write permissions.
  - Ensure that each camera is properly set up in the scene.

## Contributing

Contributions to MultiCam Auto Render Pro are welcome! Please follow the standard fork-pull request workflow:
- Fork the repository.
- Make your changes.
- Submit a pull request detailing the changes and improvements.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Contact

For support or to contact the developers, please [open an issue](https://github.com/your-github-username/multicam_auto_render_pro/issues) on GitHub.
