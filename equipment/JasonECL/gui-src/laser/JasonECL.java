package laser;
import gnu.io.*;

public class JasonECL 
{	
	public JasonECL(int com_port, boolean verbose) throws Exception
	{
		try
		{
			// Open serial port
			ser = (SerialPort) CommPortIdentifier.getPortIdentifier(String.format("COM%d", com_port)).open("ECL", 1);
			ser.setSerialPortParams(921600, SerialPort.DATABITS_8, SerialPort.STOPBITS_1, SerialPort.PARITY_NONE);
		}
		catch (NoSuchPortException e)
		{
			throw new Exception(String.format("COM%d port does not exist", com_port));
		}
		
		// Set software flow control		
		ser.setFlowControlMode(SerialPort.FLOWCONTROL_XONXOFF_OUT | SerialPort.FLOWCONTROL_XONXOFF_IN);
		this.verbose = verbose;
		this.first = true;
		this.last_pos = pos_0;
	}
	
	/**
	 * Calls the equivalent of ecl_home
	 * @throws Exception
	 */
	public synchronized void home() throws Exception
	{
		ser.getOutputStream().write("1OR\r\n".getBytes());
		if (verbose)
		{
			System.out.println("Waiting 30 seconds for ECL to stabilize");
		}
		Thread.sleep(30000);
	}
	
	public synchronized void close()
	{
		if (ser != null)
			ser.close();
	}
	
	/**
	 * Sets the position of the DC motor
	 */
	public synchronized void setPos(double pos) throws Exception
	{
		if ((pos > pos_0) || (pos < pos_6))
			throw new Exception(String.format("ECL motor position must be between %.1f and %.1f", pos_6, pos_0));
	    ser.getOutputStream().write(String.format("1PA%.3f\r\n", pos).getBytes());
	}

	/**
	 * Returns the current position of the DC motor
	 * @return position
	 */
	public synchronized double getPos() throws Exception
	{
    	byte[] buf = new byte[100];
    	// Send a request for its current position
    	ser.getOutputStream().write("1TP\r\n".getBytes());
    	// Wait while that request is in progress
    	Thread.sleep(100);
    	// Read the buffer
    	ser.getInputStream().read(buf);
    	// Convert into a double position
    	return Double.parseDouble(new String(buf).substring(3));
	}
	
	/**
	 * Set the wavelength of the laser
	 * @param wavelength in nm
	 * @throws Exception
	 */
	public synchronized void setLambda(double wavelength, boolean wait) throws Exception
	{
		if ((wavelength > pos_6_wav) || (wavelength < pos_0_wav))
			throw new Exception(String.format("ECL wavelength must be between %.1f and %.1f", pos_0_wav, pos_6_wav));
    
	    double pos = lambdaToPos(wavelength);

		if (verbose)
	        System.out.println(String.format("Setting to wavelength %.3f, position %.3f", wavelength, pos));
	    
	    // If it is the first time I've used this laser, get the current motor position
	    if (first)
	    {
	    	first = false;
	    	last_pos = getPos();
	    }

	    setPos(pos);
	    if (wait)
	    {
	        // It takes a while to move the actual laser, so I will set an extra wait time based on how far it is
	        Thread.sleep(200 + (long) (4000 * Math.abs(pos - last_pos)));
	        last_pos = pos;
	    }
	}
	
	/**
	 * Returns the wavelength of the laser
	 * @throws Exception
	 */
	public synchronized double getLambda() throws Exception
	{
		return posToLambda(getPos());
	}
	
	/**
	 * Converts the wavelength to a motor position
	 * @param wavelength
	 * @return the motor position corresponding to the wavelength
	 */
	public static double lambdaToPos(double wavelength)
	{
		return (pos_6 - pos_0) * (wavelength - pos_0_wav) / (pos_6_wav - pos_0_wav) + pos_0;
	}
	
	/**
	 * Converts the motor position to a wavelength
	 * @param position
	 * @return the wavelength corresponding to the motor position
	 */
	public static double posToLambda(double pos)
	{
		return (pos - pos_0) * (pos_6_wav - pos_0_wav) / (pos_6 - pos_0) + pos_0_wav; 
	}
	
	/**
	 * Self-test the laser
	 */
	public static void selfTest()
	{
		// The motor maybe allows around 10pm of accuracy
		double margin = 0.010;
		try
		{
			JasonECL laser = new JasonECL(3, true);
			laser.home();
    	    for (double wavelength = 1180; wavelength < 1190; wavelength += 0.5)
    	    {
    	        laser.setLambda(wavelength, true);
    	        double real_wavelength = JasonECL.posToLambda(laser.getPos());
    	        if ((wavelength < real_wavelength - margin) || (wavelength > real_wavelength + margin))
    	        	System.out.println(String.format("Self-test Error: expected %.2f, got %.2f",
    	        			wavelength, real_wavelength));
    	    }
    	    laser.close();
		}
		catch (Exception e)
		{
			System.out.println(e.getMessage());
		}
	}

	// Serial port used to communicate
	private SerialPort ser;	
	// State-keeping variables
	private boolean verbose;
	private boolean first;
	private double last_pos;

	private static final double pos_0 = 6.0;
	private static final double pos_6 = 0.0;
	// 12 August 2013 Calibration - Chen
	// LD Current = 300 mA
	public static final double pos_0_wav = 1161.6;
	public static final double pos_6_wav = 1254.5;	
	// 12 June 2012 Calibration - JSO
	// LD Current = 300 mA
	// public static final double pos_0_wav = 1161.5
	// public static final double pos_6_wav = 1253.5
}
