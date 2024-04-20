package microwave;
import java.util.List;
import java.util.Map;

import static org.junit.Assert.*;

import cucumber.api.DataTable;
import cucumber.api.Delimiter;
import cucumber.api.java.en.Given;
import cucumber.api.java.en.When;
import junit.framework.Assert;
import cucumber.api.java.en.Then;

public class Stepdefs {

	public Microwave microwave;

	public void printDigits(byte [] digits) {
    	System.out.println("Digits is: " + 
    			digits[DisplayController.TENS_OF_MINUTES] + " " + 
    			digits[DisplayController.MINUTES] + " " + 
    			digits[DisplayController.TENS_OF_SECONDS] + " " + 
    			digits[DisplayController.SECONDS]);
	}
	
	public void printStatus() {
		printDigits(microwave.digits());
		System.out.println("Mode is: " + microwave.getMode()); 
	}

/*	
	@Given("^presets are$")
    public void presets_are(DataTable arg1) throws Throwable {
		// Write code here that turns the phrase above into concrete actions
        // For automatic transformation, change DataTable to one of
        // List<YourType>, List<List<E>>, List<Map<K,V>> or Map<K,V>.
        // E,K,V must be a scalar (String, Integer, Date, enum etc)
    	List<Preset> presets; 
    	presets = arg1.asList(Preset.class);    	
		microwave = new Microwave(new ModeController(), new DisplayController(100), presets);
    	microwave.setDoorOpen(false);
		presets.stream().forEach(p -> System.out.println(p));
    }
*/
	@Given("^presets are$")
    public void presets_are(List<Preset> presets) throws Throwable {
		microwave = new Microwave(new ModeController(), new DisplayController(100), presets);
    	microwave.setDoorOpen(false);
		presets.stream().forEach(p -> System.out.println(p));
    }
	
	@Given("^foobars are$")
    // public void presets_are(List<List<String>> arg) throws Throwable {
    public void foobars_are(DataTable arg) throws Throwable {
		List<List<String>> doubleList = arg.raw(); 
		List<Map<String, String>> keyValueList = arg.asMaps(String.class, String.class);
		System.out.println("foobars (as list list) are: " + doubleList);
		System.out.println("foobars (as list map) are: " + keyValueList.toString());
		// System.out.println("This next one will fail!");
		// System.out.println("foobars (as map) are:" + arg.asMap(String.class, String.class));
	}
	
	
    @Given("^polling rate is (\\d+) ms$")
    public void polling_rate_is_ms(int rate) throws Throwable {
    	microwave.setTickRateInHz(rate);
        // System.out.println("polling rate is " + rate + " ms.");
    }

	@Given("^([A-Za-z]+) presses the (\\d+) key$")
    public void user_presses_the_key(String user, int key) throws Throwable {
        // System.out.println(user + " presses the " + key + " key.");
        microwave.digitPressed(key); 
        microwave.tick();
        // printStatus();
	}

	@Given("^([A-Za-z]+) presses the following keys: (.*)$")
	public void user_presses_keys(String user, @Delimiter(" ") List<Integer> keys) {
        // System.out.println(user + " presses the following keys: " + keys.toString());
		for (Integer key: keys) {
			microwave.digitPressed(key);
			microwave.tick();
		}
	}

	@Given("^([A-Za-z]+) presses the following keys as a table:")
	public void user_presses_keys_table(String user, List<Integer> keys) {
        // System.out.println(user + " presses the following keys (using a table): " + keys.toString());
		for (Integer key: keys) {
			microwave.digitPressed(key);
			microwave.tick();
		}
	}
	
    @When("^([A-Za-z]+) presses the start key$")
    public void user_presses_the_start_key(String user) throws Throwable {
        // System.out.println(user + " presses the start key.");
        microwave.startPressed();
        microwave.tick();
        // printStatus();
    }

    @When("^(\\d+) seconds elapse$")
    public void seconds_elapse(int time) throws Throwable {
        // System.out.println("" + time + " seconds elapse.");
        for (int i = 0; i < (time*1000) / microwave.getTickRateInHz(); i++) {
        	microwave.tick(); 
        }
        // printStatus();
    }

    @Then("^digits reads (\\d)(\\d)(\\d)(\\d)$")
    public void digits_reads(int tensOfMinutes, int minutes, int tensOfSeconds, int seconds) throws Throwable {
    	// System.out.println("Digits expects: " + tensOfMinutes + " " + minutes + " " + tensOfSeconds + " " + seconds);
    	byte [] digits = microwave.digits();
    	// printDigits(digits);
    	assertEquals((int)digits[DisplayController.TENS_OF_MINUTES], tensOfMinutes);
    	assertEquals((int)digits[DisplayController.MINUTES], minutes);
    	assertEquals((int)digits[DisplayController.TENS_OF_SECONDS], tensOfSeconds);
    	assertEquals((int)digits[DisplayController.SECONDS], seconds); 
    }

    @Then("^mode is cooking$")
    public void mode_is_cooking() throws Throwable {
    	// System.out.println("Mode is cooking");
    	assertEquals(microwave.getMode(), ModeController.Mode.Cooking);
    }

    @Then("^mode is setup$")
    public void mode_is_setup() throws Throwable {
    	// System.out.println("Mode is setup");
    	assertEquals(microwave.getMode(), ModeController.Mode.Setup);
    }

    @Then("^mode is suspended$")
    public void mode_is_suspended() throws Throwable {
    	// System.out.println("Mode is suspended");
    	assertEquals(microwave.getMode(), ModeController.Mode.Suspended);
    }

    @Given("^Bob presses the (\\d+) scenario key$")
    public void bob_presses_the_scenario_key(int arg1) throws Throwable {
    	microwave.presetPressed(arg1);
    }


    @When("^Bob presses the (\\d+) scenario key it will out-of-range fail$")
    public void bob_presses_the_scenario_key_it_will_out_of_range_fail(int arg1) throws Throwable {
        try {
        	microwave.presetPressed(arg1);
        	fail("Test should have failed with out-of-range exception");
        } catch (IllegalArgumentException e) { }
    }

    @Then("^Bob presses the (\\d+) scenario key it will mode fail$")
    public void bob_presses_the_scenario_key_it_will_mode_fail(int arg1) throws Throwable {
        try {
        	microwave.presetPressed(arg1);
        	fail("Test should have failed with mode exception");
        } catch (IllegalArgumentException e) { }
    }

    @When("^Bob presses the clear key$")
    public void bob_presses_the_clear_key() throws Throwable {
    	microwave.clearPressed();
		microwave.tick();
    }

}
