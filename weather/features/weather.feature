Feature: Retrieve weather info
  # Get the current information of
  # Blois, FR and Salt Lake City, US in Celsius and Fahrenheit

#  Scenario: Retrieve the weather info for Blois, FR in Celsius
#    Given I choose "City" for type, enter "Blois", and choose "FR" for country and  "Celsius" for unit
#    When I click on OK
#    Then I should see the weather info for "Blois, FR"


  Scenario Outline: Successful cases
    Given I choose "<enquiry_type>" for type, enter "<enquiry_param>", and choose "<country_code>" for country and  "<temperature_unit>" for unit
    Then  I should see the weather info for "<city_country>" in "<temperature_unit>"

    Examples: Location info
            | enquiry_type | enquiry_param | country_code | temperature_unit | city_country          |
            | City         | Blois         | FR           | Celsius          | Blois, FR             |
            | Zip Code     | 84102         | US           | Fahrenheit       | Salt Lake City, US    |



  Scenario Outline: Failure cases
    Given I choose "<enquiry_type>" for type, enter "<enquiry_param>", and choose "<country_code>" for country and  "<temperature_unit>" for unit
    Then  I should see the error page for "<city_country>" in "<temperature_unit>"

    Examples: Location info
            | enquiry_type | enquiry_param | country_code | temperature_unit | city_country |
            | City         | Blois         | US           | Fahrenheit       | Blois, US    |
            | Zip Code     | 84102         | FR           | Celsius          | 84102, FR    |
            | City         | 84102         | US           | Fahrenheit       | 84102, US    |
            | Zip Code     | Blois         | FR           | Celsius          | Blois, FR    |