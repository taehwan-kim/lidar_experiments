package gui;

import java.awt.FlowLayout;
import java.awt.BorderLayout;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JButton;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JSeparator;
import javax.swing.border.EmptyBorder;

import laser.JasonECL;
import java.awt.event.KeyEvent;

/**
 * A simple GUI that controls what wavelength the laser is at while
 * simultaneously showing the actual wavelength the laser is currently at
 * @author DrunkenMan
 *
 */
public class LaserGUI extends JFrame 
{
	public LaserGUI(int comPort)
	{
		super("ECL Control GUI");
		initialize();
		setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
		
		laserStep = 1.00;
		laserSet = 1200.00;
		laserReal = 1200.00;
		connected = false;
		
		update();

		this.pack();
		setResizable(false);
		setVisible (true);
		
		this.comPort = comPort;
		this.requestFocus();
	}

	private void initialize()
	{
		LaserGUIButtons buttonListener = new LaserGUIButtons(this);
		getContentPane().setLayout(new FlowLayout(FlowLayout.CENTER, 5, 5));
		
		JPanel mainPanel = new JPanel();
		mainPanel.setFocusable(false);
		getContentPane().add(mainPanel);
		mainPanel.setLayout(new BorderLayout(0, 0));
		
		JPanel ctrlPanel = new JPanel();
		ctrlPanel.setFocusable(false);
		ctrlPanel.setLayout(new BorderLayout(0, 0));
		
		ctrlUp = new JButton("^");
		ctrlUp.setFocusable(false);
		ctrlUp.setMnemonic(KeyEvent.VK_UP);
		ctrlDown = new JButton("v");
		ctrlDown.setFocusable(false);
		ctrlDown.setMnemonic(KeyEvent.VK_DOWN);
		ctrlLeft = new JButton("<");
		ctrlLeft.setFocusable(false);
		ctrlLeft.setMnemonic(KeyEvent.VK_LEFT);
		ctrlRight = new JButton(">");
		ctrlRight.setFocusable(false);
		ctrlRight.setMnemonic(KeyEvent.VK_RIGHT);
		
		ctrlUp.addActionListener(buttonListener);
		ctrlDown.addActionListener(buttonListener);
		ctrlLeft.addActionListener(buttonListener);
		ctrlRight.addActionListener(buttonListener);
		
		ctrlPanel.add(ctrlUp, BorderLayout.NORTH);
		ctrlPanel.add(ctrlDown, BorderLayout.SOUTH);
		ctrlPanel.add(ctrlLeft, BorderLayout.WEST);
		ctrlPanel.add(ctrlRight, BorderLayout.EAST);
		
		mainPanel.add(ctrlPanel, BorderLayout.WEST);
		
		stepWave = new JLabel("0.01 nm");
		stepWave.setFont(new Font("Courier New", Font.BOLD, 18));
		ctrlPanel.add(stepWave, BorderLayout.CENTER);
		
		buttonPanel = new JPanel();
		buttonPanel.setFocusable(false);
		mainPanel.add(buttonPanel, BorderLayout.NORTH);
		buttonPanel.setLayout(new FlowLayout(FlowLayout.CENTER, 5, 5));

		buttonConnect = new JButton("Connect");
		buttonConnect.setFocusable(false);
		buttonDisconnect = new JButton("Disconnect");
		buttonDisconnect.setFocusable(false);
		buttonHome = new JButton("Home");
		buttonHome.setFocusable(false);
		buttonQuit = new JButton("Quit");
		buttonQuit.setFocusable(false);
		
		buttonConnect.addActionListener(buttonListener);
		buttonDisconnect.addActionListener(buttonListener);
		buttonHome.addActionListener(buttonListener);
		buttonQuit.addActionListener(buttonListener);

		buttonPanel.add(buttonConnect);
		buttonPanel.add(buttonDisconnect);
		
		buttonPanel.add(buttonHome);
		buttonPanel.add(buttonQuit);
		
		status = new JLabel("Status: Disconnected");
		mainPanel.add(status, BorderLayout.SOUTH);
		
		JPanel setPanel = new JPanel();
		setPanel.setFocusable(false);
		setPanel.setBorder(new EmptyBorder(5, 5, 5, 5));
		setPanel.setLayout(new BorderLayout(0, 0));
		mainPanel.add(setPanel, BorderLayout.CENTER);
		
		setWave = new JLabel();
		setPanel.add(setWave, BorderLayout.NORTH);
		setWave.setFont(new Font("Courier New", Font.BOLD, 40));
		
		setWave.setText("Set: 1180.000 nm");
		realWave = new JLabel();
		setPanel.add(realWave, BorderLayout.SOUTH);
		realWave.setFont(new Font("Courier New", Font.BOLD, 40));
		realWave.setText("Act: 1180.123 nm");
		
		separator = new JSeparator();
		setPanel.add(separator, BorderLayout.CENTER);

		new LaserMouse(this);
		new LaserKeyboard(this);
	}
	
	// Connect to the laser
	public void connect()
	{
		if (!connected)
		{
			try
			{
				laser = new JasonECL(comPort, false);
				monitor = new LaserMonitor(this, laser);
				monitor.start();
				connected = true;
			}
			catch (Exception e)
			{
				JOptionPane.showMessageDialog(this, e.getMessage(), "Error", JOptionPane.WARNING_MESSAGE);
			}
		}
		update();
	}
	
	// Disconnect from the laser
	public void disconnect()
	{
		try
		{
			if (connected)
			{
				monitor.finish();
				monitor.join();
				laser.close();
				connected = false;
			}
		}
		catch (Exception e)
		{
			JOptionPane.showMessageDialog(this, e.getMessage(), "Error", JOptionPane.WARNING_MESSAGE);
		}
		update();
	}
	
	// Send the home command
	public void laserHome() { monitor.home(); }
	// Get the set wavelength
	public double getSetWave() { return laserSet; }
	// Set the actual wavelength
	public void setRealWave(double wavelength) { laserReal = wavelength; update(); }
	// Simple functions to change laser steps and the set wavelength
	public void stepUp() { laserStep = (laserStep < 10.00) ? laserStep * 10.0 : laserStep; update(); }
	public void stepDown() { laserStep = (laserStep > 0.01) ? laserStep / 10.0 : laserStep; update(); }
	public void setUp() { laserSet = (laserSet + laserStep < JasonECL.pos_6_wav) ? laserSet + laserStep : laserSet; update(); }
	public void setDown() { laserSet = (laserSet - laserStep > JasonECL.pos_0_wav) ? laserSet - laserStep : laserSet; update(); }
	
	// Updates all buttons and labels
	public void update()
	{
		setWave.setText(String.format("Set: %8.3f nm", laserSet));
		stepWave.setText(String.format("St:\n%6.3f nm", laserStep));
		
		if (connected)
		{
			buttonConnect.setEnabled(false);
			buttonDisconnect.setEnabled(true);
			buttonHome.setEnabled(true);
			if (laserReal > 0)
				realWave.setText(String.format("Act: %8.3f nm", laserReal));
			else
				realWave.setText(String.format("Act: Disabled"));
			status.setText("Status: Connected");
		}
		else
		{
			buttonConnect.setEnabled(true);
			buttonDisconnect.setEnabled(false);
			buttonHome.setEnabled(false);				
			realWave.setText(String.format("Act: Disc N/A"));
			status.setText("Status: Disconnected");
		}
	}

	private JLabel setWave;
	private JLabel realWave;
	private JLabel stepWave;
	private JLabel status;
	
	private JButton buttonHome, buttonQuit, buttonConnect, buttonDisconnect;
	private JButton ctrlUp, ctrlDown, ctrlLeft, ctrlRight;
	private JPanel buttonPanel;
	private JSeparator separator;
	
	// Whether the laser is connected or not
	private boolean connected;
	// Laser wavelength step size, set wavelength, and real wavelength
	private double laserStep, laserSet, laserReal;
	// The laser object
	private JasonECL laser;
	// The thread monitoring the laser
	private LaserMonitor monitor;
	// COM Port the laser is on
	private int comPort;
}

class LaserGUIButtons extends EventsHelper<LaserGUI> implements ActionListener
{
	LaserGUIButtons(LaserGUI gui)
	{
		super(gui);
	}
	
	public void actionPerformed(ActionEvent e) 
	{
		if (e.getActionCommand() == "Connect") { owner.connect(); }
		else if (e.getActionCommand() == "Disconnect") { owner.disconnect(); }
		else if (e.getActionCommand() == "Home") { owner.laserHome(); }
		else if (e.getActionCommand() == "Quit")
		{
			owner.disconnect();
			System.exit(0);
		}
		else if (e.getActionCommand() == "^") { owner.setUp(); }
		else if (e.getActionCommand() == "v") { owner.setDown(); }
		else if (e.getActionCommand() == "<") { owner.stepUp(); }
		else if (e.getActionCommand() == ">") { owner.stepDown(); }
		
		else throw new Error("Internal Error: " + e.getActionCommand() + "' is not supported!");
	}

}
