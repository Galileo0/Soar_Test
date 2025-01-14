Feature: User Registration and Login

  # Scenario 1: User Registration
  Scenario Outline: Register a user with random details
    Given the user provides registration details with name "<fullName>", username "<userName>", email "<email>", password "<password>", and phone "<phone>"
    When the user registers via the "<endpoint>" endpoint
    Then the registration response should have status code 200

    Examples:
      | fullName     | userName   | email               | password    | phone     | endpoint             |
      | John Men     | jdoe       | john@gmail.com     | Password@123 | 1234567890 | /client_registeration |
      | Alice tudor  | asmith     | alice@gmail.com    | Password@456 | 0987654321 | /client_registeration |
      | Bob Rans  | bjohnson   | Bob@gmail.com  | Password@789 | 1122334455 | /client_registeration |

  # Scenario 2: User Login
  Scenario Outline: Login with valid credentials
    Given the user provides login details with userName "<userName>", email "<email>", and password "<password>"
    When the user logs in via the "<endpoint>" endpoint
    Then the login response should have status code 200

    Examples:
      | userName           | email                | password    | endpoint        |
      | jdoe               | john@gmail.com       | Password@123 | /client_login   |
      | asmith             | alice@gmail.com      | Password@456 | /client_login   |
      | bjohnson           | bob@gmail.com        | Password@789 | /client_login   |
