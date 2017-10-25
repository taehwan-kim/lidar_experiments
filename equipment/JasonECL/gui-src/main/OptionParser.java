package main;

import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;

/**
 * Option Parser
 * @author Owen Chen, converted to Java from C++
 *
 */
class OptionParser extends HashMap<String, String>
{
	protected ArrayList<String> option_names;
	HashMap<String, OptionInfo> option_infos;
	
    public OptionParser()
    {
    	option_names = new ArrayList<String>();
    	option_infos = new HashMap<String, OptionInfo>();
    }
    
    /**
     * Add an option to the option parser
     */
    public void addOption(String option_name, String var_name,
    		boolean has_arg, String arg_name, boolean has_default_arg_value, String default_arg_value,
    		String description)
    {
    	OptionInfo option_info = new OptionInfo(var_name, has_arg, arg_name, has_default_arg_value,
    			default_arg_value, description);
    	
    	if (option_infos.containsKey(option_name)) throw new Error("Option exists: " + option_name);
    	
        // Add the option name to an array for sorting
    	option_names.add(option_name);

        // Add option info 
        option_infos.put(option_name, option_info);

        // Set the default argument value
        if(has_default_arg_value)
            put(var_name, default_arg_value);    	
    }
    
    public void parseArguments(String[] args, PrintStream err, PrintStream out)
    {
        boolean is_print_options = false;
        int arg_idx = 0;

        while(arg_idx < args.length)
        {
            String option_name = args[arg_idx];

            // Print the options page if -help is specified
            if(option_name.equals("-help"))
            {
                is_print_options = true;
                break;
            }
            else if(option_infos.containsKey(option_name))
            {
                OptionInfo option_info = option_infos.get(option_name);
                String var_name = option_info.getVarName();
                if(option_info.hasArg())
                {
                    if((arg_idx + 1) >= args.length)
                    {
                    	err.println("[Error] Missing argument for option: '" + option_name + "'");
                        is_print_options = true;
                        break;
                    }

                    String option_arg = args[arg_idx + 1];
                    put(var_name, option_arg);
                    
                    arg_idx += 2;
                }
                else
                {
                    // If the option does not require an argument
                    // then set it to true
                    put(var_name, "true");

                    arg_idx += 1;
                }
            }
            else
            {
                err.println("[Error] Unknown option: '" + option_name + "'");
                is_print_options = true;
                break;
            }
        }

        // Check if all required options are set (the ones without default values)
        Iterator<String> it = option_names.iterator();
        while(it.hasNext())
        {
            String option_name = it.next();
            OptionInfo option_info = option_infos.get(option_name);

            if(!option_info.hasDefaultArgValue())
            {
                String var_name = option_info.getVarName();
                if(!containsKey(var_name))
                {
                    err.println("[Error] Missing required option: '" + option_name + "'");
                    is_print_options = true;
                }
            }
        }

        if(is_print_options)
        {
            printOptions(out);
            System.exit(0);
        }
        return;
    }
    public void printOptions(PrintStream out)
    {
        out.println();
        out.println("Available options:");
        out.println("==================");
        out.println();

        Iterator<String> it = option_names.iterator();
        while(it.hasNext())
        {
            String option_name = it.next();
            OptionInfo option_info = option_infos.get(option_name);

            out.print(option_name);
            if(option_info.hasArg())
            {
                out.print(" <" + option_info.getArgName() + ">");
            }
            out.println();

            out.println("    " + option_info.getDescription());
            if(option_info.hasArg() && option_info.hasDefaultArgValue())
            {
                out.println("    " + "Default: " + option_info.getDefaultArgValue());
            }
            out.println();
        }
        out.println("-help");
        out.println("    " + "Print this page");
        out.println();
        return;
    }
}

class OptionInfo
{
    public OptionInfo(String var_name, 
    		boolean has_arg, String arg_name, boolean has_default_arg_value, String default_arg_value,
    		String description)
    {
    	this.var_name = var_name;
    	this.has_arg = has_arg;
    	this.arg_name = arg_name;
    	this.has_default_arg_value = has_default_arg_value;
    	this.default_arg_value = default_arg_value;
    	this.description = description;
    	
    }

	private String var_name;
	private boolean has_arg;
	private String arg_name;
	private boolean has_default_arg_value;
	private String default_arg_value;
	private String description;

	public String getVarName() { return var_name; }
    public boolean hasArg() { return has_arg; }
    public String getArgName() { return arg_name; }
    public boolean hasDefaultArgValue() { return has_default_arg_value; }
    public String getDefaultArgValue() { return default_arg_value; }
    public String getDescription() { return description; }
    
};
