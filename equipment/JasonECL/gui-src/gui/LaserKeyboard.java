package gui;

import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

public class LaserKeyboard implements KeyListener
{
	// The gui the listener is a part of
	LaserGUI gui;
	
	public LaserKeyboard(LaserGUI gui)
	{
		this.gui = gui;
		gui.addKeyListener(this);
	}

	public void keyPressed(KeyEvent e)
	{
		switch(e.getKeyCode())
		{
			// Left Arrow
			case 37: gui.stepUp();
				break;
			// Up Arrow
			case 38: gui.setUp(); 
				break;
			// Right Arrow
			case 39: gui.stepDown(); 
				break;
			// Down Arrow
			case 40: gui.setDown(); 
				break;
//			// Pg Up
//			case 33: gui.getRender().zoom(1.2);
//				break;
//			// Pg Down
//			case 34: gui.getRender().zoom(1 / 1.2);
//				break;
//			// Home
//			case 36: gui.getRender().zoom();
		}
	}

	public void keyReleased(KeyEvent e) {
		
	}

	public void keyTyped(KeyEvent e) {
//		System.out.println(e.getKeyChar());
		
	}
		
}
