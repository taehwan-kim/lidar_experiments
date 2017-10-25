package gui;

import java.awt.event.MouseEvent;
import java.awt.event.MouseWheelEvent;
import java.awt.Cursor;

import javax.swing.JPanel;
import javax.swing.event.MouseInputAdapter;

public class LaserMouse extends MouseInputAdapter 
{	
	// The scaling step size
	public static final double SCALE_STEP = 1.1;
	
	// The gui the listener is a part of
	LaserGUI gui;
	
	public LaserMouse(LaserGUI gui)
	{
		this.gui = gui;
		gui.addMouseListener(this);
		gui.addMouseWheelListener(this);
		gui.addMouseMotionListener(this);
	}
	
	/**
	 * Turn the mouse into a crosshair when entering the gui
	 */
	public void mouseEntered(MouseEvent e)
	{
		gui.setCursor(new Cursor(Cursor.CROSSHAIR_CURSOR));
	}

	/**
	 * Turn the mouse into the default mouse when exiting the gui
	 */
	public void mouseExited(MouseEvent e)
	{
		gui.setCursor(new Cursor(Cursor.DEFAULT_CURSOR));
	}
	
	public void mouseMoved(MouseEvent e)
	{}
	
	
	public void mouseClicked(MouseEvent e)
	{}
	
	public void mouseWheelMoved(MouseWheelEvent e)
	{
		int rotate = e.getWheelRotation();
		if (rotate > 0)
			for (int i = 0; i < rotate; ++i)
				gui.setDown();
		else
			for (int i = 0; i > rotate; --i)
				gui.setUp();
	}
	
}
