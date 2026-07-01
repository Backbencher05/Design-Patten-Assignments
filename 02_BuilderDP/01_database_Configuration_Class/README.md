# Builder Pattern Implementation for a database configuration class

- Problem Statement
You are tasked with creating a system-wide database configuration for a complex software suite. The configuration is responsible for managing various configuration settings that affect the data layer. To ensure a flexible and readable way to create configuration instances that are immutable, you decide to implement the Builder pattern.

- Assignment
Your task is to implement the Builder pattern to create instances of a configuration manager class. The Builder pattern allows for step-by-step construction of complex objects while keeping the creation process separate from the main object.

The usage of your builder should look like this:

config = DatabaseBuilder()\
    .with_database_url('jdbc:postgresql://localhost:5432/mydb')\
    .with_username('user')\
    .with_password('password')\
    .build()

# Implementing the Builder Pattern

1.  Review the original class and the builder interface - You have been provided with a class that   represents the database configuration DatabaseConfiguration. The class has a number of properties that are used to configure the database connection. The class extends from the Builder interface which has a method build() that returns an instance of the class. Your task is to implement the Builder pattern to create instances of a class with the same properties. You have to complete the implementation of the build method.

2. Implement the setter methods - The idea of the builder method to have a mutable instance of the DatabaseConfiguration class in the builder class and expose methods to set the properties of the class. Once the properties have been set, the build method is called to create an immutable instance of the class. You need to implement the setter methods for the properties of the DatabaseConfiguration class in the builder class. Methods like with_database_url, with_username, with_password, etc. should be implemented so that the user can use the builder instance to set the properties of the DatabaseConfiguration class.

3. Implement the build method - The build method is responsible for creating an instance of the DatabaseConfiguration class. The method should return an instance of the DatabaseConfiguration class with the properties set by the user using the builder instance.

4. Test your implementation - A test case has been provided for you to test your implementation. Run the test case to ensure that your implementation is correct.

# Instructions
- Clone this repository to your local machine.
- Open the DatabaseConfiguration class and implement the setter methods in the DatabaseBuilder class.
- Implement the build method in the DatabaseBuilder class.
- Run the provided test cases in the TestDatabaseBuilder class to verify the correctness of your implementation.