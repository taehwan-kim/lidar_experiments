package gui;

import javax.swing.JOptionPane;

import laser.JasonECL;

/**
 * Class that is responsible for monitoring what the laser is doing and sending commands to it
 * @author DrunkenMan
 */
public class LaserMover extends Thread
{
	public LaserMover(LaserGUI gui, JasonECL laser)
	{
		this.gui = gui;
		this.laser = laser;
		this.home = false;
		this.finished = false;
	}
	
	public void run()
	{
		try
		{
			double curSetWave = laser.getLambda();
			do
			{
				// If told to go home, it will tell the laser to go home and
				// not do anything else in the meantime
				if (home)
				{
					laser.home();
					home = false;					
				}
				// Find where to move the laser to, if necessary
				double nextSetWave = gui.getSetWave();
				if (nextSetWave != curSetWave)
				{
					curSetWave = nextSetWave;
					laser.setLambda(curSetWave, true);				
				}				
			} while (!finished);
			
		}
		// If anything bad happens stop the thread and display a dialogue
		catch (Exception e)
		{
			JOptionPane.showMessageDialog(gui, e.getMessage(), "Error", JOptionPane.WARNING_MESSAGE);
		}
    }
	
	public void home()
	{
		home = true;
	}
	
	public void finish()
	{
		finished = true;
	}

	// The GUI object
	private LaserGUI gui;
	// The laser to monitor
	private JasonECL laser;
	// When set to true, the laser will be told to go home in the next loop
	private boolean home;
	// When set to true, this thread will stop looping
	private boolean finished;	
}
