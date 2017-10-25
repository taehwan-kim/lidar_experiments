package main;

import javax.swing.SwingUtilities;
import javax.swing.UIManager;
import gui.LaserGUI;

public class Main 
{
	public static void main (String[] args)
	{
//		laser.JasonECL.selfTest();
		initialize(args);
	}
	
    private static void setRuntimeOptions(OptionParser option_parser)
    {
        option_parser.addOption("-com", "port", true, "COMPORT", true, "3",
                "Specifies the COM port the laser is connected to");
    }

	private static void initialize(String[] args)
	{
		OptionParser option_parser = new OptionParser();
		setRuntimeOptions(option_parser);		
		// Parse the options
		option_parser.parseArguments(args, System.err, System.out);
		
		try
		{
            // Set System L&F
	        UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
	    } 
	    catch (Exception e)
	    {
	       // Not a big issue if we can't set the system-native look and feel
	    }
		
		SwingUtilities.invokeLater(new GUIRunnable(Integer.parseInt(option_parser.get("port"))));	
	}	
}

class GUIRunnable implements Runnable
{
	// Floorplanner GUI
	private LaserGUI gui;
	private int comPort;
	
	GUIRunnable (int comPort)
	{		
		this.comPort = comPort;
	}
	
	public void run()
	{
		gui = new LaserGUI(comPort);
	}
}
