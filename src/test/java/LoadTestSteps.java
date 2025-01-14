import io.restassured.RestAssured;
import io.restassured.response.Response;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import org.junit.jupiter.api.Assertions;

import java.util.Random;

public class LoadTestSteps {

    private String fullName;
    private String userName;
    private String email;
    private String password;
    private String phone;
    private Response response;

    // Generate random string of characters
    private String generateRandomString(int length) {
        String characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        Random random = new Random();
        StringBuilder stringBuilder = new StringBuilder();
        for (int i = 0; i < length; i++) {
            int index = random.nextInt(characters.length());
            stringBuilder.append(characters.charAt(index));
        }
        return stringBuilder.toString();
    }

    // Generate random user details with gmail.com domain for email
    private void generateRandomUserDetails() {
        fullName = generateRandomString(8) + " " + generateRandomString(5);
        userName = generateRandomString(6);
        email = generateRandomString(6) + "@gmail.com";  // Ensure email ends with gmail.com
        password = "password" + new Random().nextInt(1000); // Random password
        phone = "123456" + new Random().nextInt(1000); // Random phone number
    }

    // Step for registration with data passed from feature file
    @Given("the user provides registration details with name {string}, username {string}, email {string}, password {string}, and phone {string}")
    public void givenRegistrationDetails(String fullName, String userName, String email, String password, String phone) {
        generateRandomUserDetails();
        this.fullName = fullName != null ? fullName : this.fullName;
        this.userName = userName != null ? userName : this.userName;
        this.email = email != null ? email : this.email;
        this.password = password != null ? password : this.password;
        this.phone = phone != null ? phone : this.phone;
    }

    @When("the user registers via the {string} endpoint")
    public void the_user_registers_via_the_endpoint(String endpoint) {
        response = RestAssured.given()
                .formParam("fullName", fullName)
                .formParam("userName", userName)
                .formParam("email", email)
                .formParam("password", password)
                .formParam("phone", phone)
                .post("http://127.0.0.1:5000" + endpoint);  // Dynamically use the endpoint passed in the scenario

        // Log the response for debugging
        System.out.println("Registration response status code: " + response.getStatusCode());
        System.out.println("Registration response body: " + response.getBody().asString());
    }

    @Then("the registration response should have status code 200")
    public void thenVerifyRegistrationResponseStatus() {
        Assertions.assertEquals(200, response.getStatusCode());
    }

    // Step for login with data passed from feature file
    @Given("the user provides login details with userName {string}, email {string}, and password {string}")
    public void givenLoginDetails(String userName, String email, String password) {
        this.userName = userName != null ? userName : this.userName;
        this.email = email != null ? email : this.email;
        this.password = password != null ? password : this.password;
    }

    @When("the user logs in via the {string} endpoint")
    public void whenUserLogsIn(String endpoint) {
        // Log the login details for debugging
        System.out.println("Logging in with: userName = " + userName + ", email = " + email + ", password = " + password);

        // Make the POST request for login
        response = RestAssured.given()
                .formParam("userName", userName)
                .formParam("email", email)  // Pass email for login
                .formParam("password", password)
                .post("http://127.0.0.1:5000" + endpoint);  // Dynamically use the endpoint passed in the scenario

        // Log the response for debugging
        System.out.println("Login response status code: " + response.getStatusCode());
        System.out.println("Login response body: " + response.getBody().asString());
    }

    @Then("the login response should have status code 200")
    public void thenVerifyLoginResponseStatus() {

        System.out.println("Expected Status: 200, Actual Status: " + response.getStatusCode());
        Assertions.assertEquals(200, response.getStatusCode());

        // Additional check if response is not 200, print out details for debugging
        if (response.getStatusCode() != 200) {
            System.out.println("Error Response: " + response.getBody().asString());
            Assertions.fail("Login failed with status code " + response.getStatusCode());
        }
    }
}
