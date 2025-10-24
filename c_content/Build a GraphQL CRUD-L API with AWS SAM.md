# Build a GraphQL CRUD-L API with AWS SAM

## Overview
This course will guide you through the process of building a serverless GraphQL API. 

The application you will build is a weather application that will perform **(CRUD-L) *create, read, update, delete, and list*** operations. 

The application utilizes various AWS resources, including Lambda functions, a DynamoDB Database, and AWS AppSync. 

You will use AWS SAM for resource and infrastructure provisioning.

## Description
This course will guide you through the process of building a serverless GraphQL API. The application you will build is a weather application that will perform (CRUD-L) create, read, update, delete, and list operations. The application utilizes various AWS resources, including Lambda functions, a DynamoDB Database, and AWS AppSync. You will use AWS SAM for resource and infrastructure provisioning.

## Course Details
- **Number of Modules:** 11
- **Image:** https://d14x58xoxfhz1s.cloudfront.net/6948e10d-0173-4b4e-82d5-de536d45fc3c
- **Difficulty:** Beginner
- **Framework:** AWS SAM
- **Programming_language:** Python
- **Web_framework:** 
- **Mobile_framework:** 
- **ServerlessTopic:** serverless_architecture
- **MainCourse:** true
- **MainCourseId:** N/A
- **Trailer:** 
- **Video:** N/A
- **File:** weather-sam-graphql-api-main.zip
- **CodeVisible:** true
- **UploadVisible:** false
- **Tasks:** false
- **Publish:** true
- **ProposedCourses:** 
- **AuthorId:** 3c926a9e-9406-45e2-98d9-006600258387
- **AuthorGroup:** admin
- **Duration:** N/A
- **Featured:** N/A
- **DefaultMedia:** N/A
- **NumberOfLessons:** 28
- **CreatedAt:** 2023-12-20T10:52:06.405Z
- **UpdatedAt:** 2024-10-12T04:30:59.396Z
- **CourseCategoryCourseId:** ac49bd8c-68fe-45c4-8b6a-37bf9ee28389
- **_version:** 10
- **_lastChangedAt:** 1728707459414
- **_deleted:** N/A

## Module 1: Create resources for the Delete Operation

### Lesson 1: Create a deleteWeather Lambda Function Resource

In this section, you will create the resources for the DELETE operation for your CRUD API.

In your `template.yaml` file, in the Resources section under your Functions resources, add the code below:

```yaml
        deleteWeatherItem:
          Runtime:
            Name: APPSYNC_JS
            Version: "1.0.0"
          DataSource: Weather
          CodeUri: ./functions/deleteWeatherItem.js      
```

I am sure at this point you have noticed that the different function resources you are creating have similar code. The code above is no different, similar to the last ones we created, except for the function name and function path.

Let us break down what this function code is doing.

The `deleteWeatheritem` resource function is responsible for handling the deletion of a created weather item.

It uses the **`APPSYNC_JS`** runtime and relies on the **`Weather`** data source, and the corresponding JavaScript code is stored in the **`deleteWeatherItem.js`** file which we will be creating in the next task. 

Still, in your `template.yaml` file, you will create another resource, a pipeline Resolver.

Enter the following code in the Resource section:

```yaml
          deleteWeather:
            Runtime:
              Name: APPSYNC_JS
              Version: "1.0.0"
            Pipeline:
              - deleteWeatherItem
```

The code above is a resolver for a type mutation named `deleteWeather` in the AWS AppSync API. 

Like the other resolvers you created, it uses the **`APPSYNC_JS`** runtime version 1.0.0 and employs a pipeline of a resolver function **`deleteWeatherItem`** to handle the mutation operation.


Please confirm that you have configured everything correctly by checking against the full code.

### Lesson 2: Create a deleteWeather Resolver Function

You have created the deleteWeather function resource, now you will need to define a function resolver for the resource you created.

Open the  `functions` folder.

Create a new file called`deleteWeatheritem.js` and paste the code below.

```jsx
import { remove } from "@aws-appsync/utils/dynamodb";

export function request(ctx) {
  const { id } = ctx.args;

  return remove({ key: { id } });
}

export function response(ctx) {
  return true;
}
```

- The code above is a resolver for a delete operation, where you're using the **`remove`** function from **`@aws-appsync/utils/dynamodb`** to delete an item from a DynamoDB based on its `id`.

- In the **`request`** function, you're extracting the **`id`** from the **`ctx.args`** object. Then, you're calling the **`remove`** function with an object containing the key to be deleted. The key is specified as an object with the **`id`** property.

- The **`response`** function simply returns **`true`**. This means that the resolver is expected to return a boolean value, to indicate the success of the delete operation.

## Module 2: Create resources for the Create Operation

### Lesson 1: Create a preprocessWeather Resolver Function

You have created the `preProcessWeather` function resource. Now, you will need to define a resolver function for the resource you created.

From your project root folder, rename the `gql` folder to `functions`.

Rename the `preprocessPostItem.js` file to `preprocessWeatheritem.js` and replace the code in that file with the code below.

```jsx
import { util } from "@aws-appsync/utils";

export function request(ctx) {
  const id = util.autoId();

  const { ...values } = ctx.args;
  values.createdOn = util.time.nowEpochMilliSeconds();

  return { payload: { key: { id }, values: values } };
}

export function response(ctx) {
  return ctx.result;
}
```

- The **`preprocessWeatherItem.js`** function will perform two operations: **`request`** and **`response`**.
- The `request` function will process an incoming request.
- It will then generate a unique identifier using **`util.autoId()`**.
- Next, it extracts values from the **`ctx.args`** object, which should contain some GraphQL arguments.
- It adds a **`createdOn`** property to the **`values`** object, representing the current epoch timestamp in milliseconds.
- Finally, it returns an object with a **`payload`** property containing a **`key`** object with the generated **`id`** and a **`values`** object with the processed values.
- The `response` function simply returns the **`result`** property from the **`ctx`** (context) object.

### Lesson 2: Create a CreateWeather Lambda Function Resource

In this section, you will create the resources for the CREATE operation for our CRUD API.

In your `template.yaml` file, in the Resources section under your Functions resources, add the code below:

```yaml
        createWeatherItem:
          Runtime:
            Name: APPSYNC_JS
            Version: "1.0.0"
          DataSource: Weather
          CodeUri: ./functions/createWeatherItem.js
```

Notice the code above is the same as the code for the `preprocessWeatherItem` function. The only difference is your function name and function path.

So, what are the key differences in these function resources you just created?

The `createWeatherItem` resource function is responsible for handling the creation of weather items.

 It uses the **`APPSYNC_JS`** runtime and relies on the **`Weather`** data source. 

The corresponding JavaScript code is stored in the **`createWeatherItem.js`** file, which we will be creating in the next task.

### Lesson 3: Create a preProcessWeather Function Resource

In the next modules, you will define the function resources in the `template.yaml` file. Add the following code in the Resources section to define the first function resource.

```yaml
Functions:
        preprocessWeatherItem:
          Runtime:
            Name: APPSYNC_JS
            Version: 1.0.0
          DataSource: NONE
          CodeUri: ./functions/preprocessWeatherItem.js
```

- `preprocessWeatherItem` is the name of the serverless function.
- `Runtime: APPSYNC_JS` The function is configured to use the `APPSYNC_JS` runtime.
- `Runtime Version: 1.0.0` This specifies the version of the runtime being used.
- `DataSource: NONE` Shows that this function doesn't rely on any specific data source. In AppSync, data sources are typically associated with backend data storage or other services.
- `CodeUri: ./functions/preprocessWeatherItem.js` Location of the JavaScript code for the function.

Still in your `template.yaml` file, you will create another Resource, a pipeline Resolver.

Enter the following code in the Resource section:

```jsx
Resolvers:
        Mutation:
          createWeather:
            Runtime:
              Name: APPSYNC_JS
              Version: "1.0.0"
            Pipeline:
              - preprocessWeatherItem
              - createWeatherItem
```

The code above is a resolver for a mutation named **`createWeather`** in the AWS AppSync API. This resolver uses the **`APPSYNC_JS`** runtime version 1.0.0 and employs a pipeline of two resolver functions, **`preprocessWeatherItem`** and **`createWeatherItem`**, to handle the mutation operation.

### Lesson 4: Create a createWeather Resolver Function

You have created the `createWeather` function resource. Now, you will need to define a function resolver for the resource you created.

Open the `functions` folder.

Rename the `createPostItem.js` file to `createWeatheritem.js` and replace the code in that file with the code below.

```jsx
import { put } from "@aws-appsync/utils/dynamodb";

export function request(ctx) {
  const { key, values } = ctx.prev.result;
  return put({
    key: key,
    item: values,
  });
}

export function response(ctx) {
  return ctx.result;
}
```

- The request operation will process a request before it is sent to DynamoDB.
- It extracts the **`key`** and **`values`** from the **`ctx.prev.result`** object. The **`ctx.prev.result`** contains the result of a previous operation in the resolver chain.
- It then uses the **`put`** operation from **`@aws-appsync/utils/dynamodb`** to construct a DynamoDB **`put`** operation.
- The **`put`** function takes an object with **`key`** (partition key and sort key) and **`item`** (values to be stored) properties.
- The created DynamoDB item is returned.

## Module 3: Create resources for the Update Operation

### Lesson 1: Create an updateWeather Resolver Function

You have created the `updateWeather` function resource. Now, you must define a function resolver for the resource you created.

Open the `functions` folder.

Rename the `greet.js` file to `updateWeatheritem.js` and replace the code in that file with the code below.

```jsx
import { update, operations } from "@aws-appsync/utils/dynamodb";

export function request(ctx) {
  const { id, weather, town } = ctx.args;

  return update({
    key: { id },
    update: {
      weather: operations.replace(weather),
      town: operations.replace(town),
      updatedOn: operations.add(util.time.nowEpochMilliSeconds()),
    },
  });
}
export function response(ctx) {
  return ctx.result;
}
```

- The code above is for an App Sync resolver mapping template function that updates items in a DynamoDB table.

- The first part of the function code is a `request` function that will perform an update operation by processing the request before it is sent to DynamoDB to update an item.

- It extracts **`id`**, **`weather`**, and **`town`** from the **`ctx.args`** object, representing an item's updated values.

- It uses the **`update`** function from **`@aws-appsync/utils/dynamodb`** to construct a DynamoDB update operation.

- The update operation specifies that the **`weather`** and **`town`** attributes should be replaced with the newly provided values, and the **`updatedOn`** attribute should be updated by adding the current epoch timestamp in milliseconds.

- The newly updated DynamoDB item is returned.

### Lesson 2: Create an updateWeather Lambda Function Resource

In this section, you will create the resources for the UPDATE operation for your CRUD API.

In your `template.yaml` file, in the Resources section under your Functions resources, add the code below:

```yaml
        updateWeatherItem:
          Runtime:
            Name: APPSYNC_JS
            Version: "1.0.0"
          DataSource: Weather
          CodeUri: ./functions/updateWeatherItem.js
```

Notice that the code above is almost the same as the code for the `createWeatherItem` function. The only difference is your function name and function path.

Let's break down what this function code is doing.

The `updateWeatherItem` resource function is responsible for handling the updating of a created weather item. It uses the **`APPSYNC_JS`** runtime and relies on the **`Weather`** data source. The corresponding JavaScript code is stored in the **`createWeatherItem.js`** file, which we will create in the next task.

Still, in your `template.yaml` file, you will create another Resource, a pipeline Resolver.

Enter the following code in the Resource section:

```yaml
updateWeather:
            Runtime:
              Name: APPSYNC_JS
              Version: "1.0.0"
            Pipeline:
              - updateWeatherItem
```

The code above is a resolver for a mutation named `updateWeather` in the AWS AppSync API. Like the first resolver created, it uses the **`APPSYNC_JS`** runtime version 1.0.0 and employs a pipeline with a resolver function **`updateWeatherItem`** to handle the mutation operation.


## Module 4: Project setup

### Lesson 1: Create a SAM project

In this module, you will create the initial skeleton of an application from which you can continue building your project.

- Initialize a SAM application by running the following command in your terminal

```yaml
sam init
```

- From the ***Which template source would you like to use*** option? Choose: ***1- AWS Quick Start Templates.***

![image](https://d14x58xoxfhz1s.cloudfront.net/712a066b-ff5f-4ab7-9607-de6441d1cf6a)

Follow the prompts and make the following selections as shown in the steps below to initialize your application.

- From the ***Choose an AWS Quick Start application template*** option, choose: ***12- GraphQLApi Hello World Example***

![image](https://d14x58xoxfhz1s.cloudfront.net/8a2bc04e-371f-499b-9b0f-63f5f6b3a9b6)

- Select (Yes) ***y*** for the rest of the prompts.
- For the ***Project name [sam app]*** option type the name you would like to use for your project and press enter.
- You should have an output like the one shown below.

![image](https://d14x58xoxfhz1s.cloudfront.net/867906bb-3b83-4df4-adbd-f8c7c150ced1)

You should have a project structure like the one below.

![image](https://d14x58xoxfhz1s.cloudfront.net/112e2f12-4562-4b76-9e84-6bd79ddec5d3)

### Lesson 2: Build and deploy

Before proceeding, it's essential that we build and deploy our "Hello World" GraphQL application to ensure everything is working well from the start.

Execute the following commands to build and deploy the SAM project.

- Open a new terminal in your IDE and run the following commands.

```
sam build
sam deploy --guided
```

The `sam build` command will build the source code of your application.

The `sam deploy --guided` command will package and deploy your application to AWS, with a series of prompts:

- **Stack Name:** The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something that matches your project name.
- **AWS Region:** The AWS region where you want to deploy your app.
- **Confirm changes before deployment**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
- **Allow SAM CLI IAM role creation**: AWS SAM templates, including creating AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to the minimum required permissions. To deploy an AWS CloudFormation stack that creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `-capabilities CAPABILITY_IAM` to the `sam deploy` command.
- **Save arguments to samconfig.toml**: If set to "yes", your choices will be saved to a configuration file inside the project. This will allow you to simply re-run `sam deploy` without any parameters in the future, to deploy changes to your application.

### Lesson 3: Explore the SAM template

To be highly effective with the SAM IaC (Infrastructure as Code), it's essential to learn the basic building blocks of a SAM template.

AWS SAM is a high-level abstraction of AWS CloudFormation, so when you build a SAM template, it compiles to CloudFormation resources.

Here are the main sections of a SAM template file.

***Transform declaration***

This declaration identifies an AWS CloudFormation template file as an AWS SAM template file, and it has the following declaration: `Transform: AWS::Serverless-2016-10-31`, which is required for all SAM templates.

***Globals section***

This section is unique to AWS SAM and defines properties that are common to all of your serverless functions and APIs.

We'll see how to use properties in this section to effectively build our API.

***Resources section***

In AWS SAM templates, the Resources section can contain a combination of AWS CloudFormation resources and AWS SAM resources.

***Parameters section***

Objects declared in the Parameters section cause the `sam deploy --guided` command to present additional prompts to the user.

Let's proceed to create our API, functions, and database by defining resources in the resources section of the SAM template file.

## Module 5: Create SAM API resources

### Lesson 1: Create graphql api

Next, you will create the GraphQL API resource.

In the `template.yaml` file, under `Resources`, add the following YAML code:

```yaml
WeatherGraphQLApi:
    Type: AWS::Serverless::GraphQLApi
    Properties:
      SchemaUri: ./schema/schema.graphql
      Auth:
        Type: API_KEY
      ApiKeys:
        MyApiKey:
          Description: weather api key
      DataSources:
        DynamoDb:
          Weather:
            TableName: !Ref WeatherTable
            TableArn: !GetAtt WeatherTable.Arn
```

`WeatherGraphQLApi` is the logical name for the AWS Serverless GraphQL API resource.

`Type: AWS::Serverless::GraphQLApi` specifies the CloudFormation resource type for the GraphQL API.

`Properties` This section contains the configuration properties for the GraphQL API.

`SchemaUri: ./schema/schema.graphql` specifies the location of the GraphQL schema file. 

`Auth` specifies the authentication configuration for the GraphQL API.

`Type: API_KEY` configures API key authentication for the GraphQL API.

`ApiKeys` defines the API keys associated with the GraphQL API.

`MyApiKey` is a logical name for the API key.

`Description:weather api key`  description for the API key.

`DataSources:` This section defines the data sources for the GraphQL API.

`DynamoDb:`  configures a data source named `Weather` using DynamoDB.

`Weather:` logical name for the DynamoDB data source.

`TableName: !Ref WeatherTable:` specifies the DynamoDB table name by referencing the logical name `WeatherTable.`

`TableArn: !GetAtt WeatherTable.Arn:`  retrieves the Amazon Resource Name (ARN) of the DynamoDB table using the logical name 

`WeatherTable` and the attribute `Arn.`

The above code sets up a Serverless GraphQL API with API key authentication, and it uses DynamoDB as a data source for weather-related data.

### Lesson 2: Create weather table

Now that you have created a skeleton for your project and explored your `template.yaml` file, this is the main part of the project that you will edit to build your resources for this project. Let's go ahead and start creating the resources you will need for your project.

You will be storing the weather details in a DynamoDB table.

Go ahead and create this table in the resources section of your `template.yaml` file.

Under `Resources`, type in the following YAML code:

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31
Description: >
  sam-app-gql

  Sample SAM Template for sam-app-gql

Resources:
  WeatherTable:
    Type: AWS::Serverless::SimpleTable
```

`WeatherTable` is the logical ID of our DynamoDB table. `Type` is the resource type, which is `AWS::DynamoDB::Table`.

In essence, the code above is creating a serverless application with a single resource - a DynamoDB table (**`WeatherTable`**) defined using the **`AWS::Serverless::SimpleTable`** resource type.

## Module 6: Test

### Lesson 1: Testing the Delete Operation

- Let's proceed to test the Delete operation.
- From your DynamoDB table, copy the `id` of an item you would like to delete.

![WeatherGQL 15  remember to explain the updated on attr.png](https://d14x58xoxfhz1s.cloudfront.net/318a82e3-162d-41ea-a6cb-246c1ec6945e)

- Under the `mutation MyMutation`, select the `deleteWeather` mutation type and check the `id` box. Insert the `id` value you copied from the DynamoDB table.
- Run the mutation.
- You should receive a `true` response to indicate that the item you selected has been successfully deleted.

![WeatherGQL 16 del op.png](https://d14x58xoxfhz1s.cloudfront.net/f72c191e-60ae-45a6-b445-c55cc046497f)

- Confirm that the item you deleted has been successfully removed from the DynamoDB table.

![WeatherGQL 17 confirm del in dynadb.png](https://d14x58xoxfhz1s.cloudfront.net/bd0b5a59-ba8b-41d3-b304-beac33812c48)

- *Congratulations, you have successfully deleted a weather item.*

### Lesson 2: Testing create weather operation

You have confirmed that your resources have been deployed to the cloud. Now, you will explore testing methods for your GraphQL API.

By the end of this testing module, you will have confidence that your API works as intended.

- First, you will test the Create operation.
- From the AppSync console tab that you left open, where your APIs are listed, open your `WeatherGraphQLApi` and select **Run a query**.

![WeatherGQL 2.png](https://d14x58xoxfhz1s.cloudfront.net/257c3625-0a18-4781-8933-fd13f7751778)

The AWS AppSync console provides a query editor where you can interact with your API without having to write code to initiate the GraphQL request. You are going to test a few of our mutations and queries to ensure that the API is working as desired.

- From the AppSync query editor, select "Mutation" from the drop-down in the Explorer window.
- Under the `mutation MyMutation`, select the `createWeather` mutation type and check all the boxes as shown in the image below.

![WeatherGQL 4.png](https://d14x58xoxfhz1s.cloudfront.net/4e928deb-9596-4ace-996f-f41eb87af9f4)

You will now create a weather item by specifying the name of a town and its weather. In my case, I created a weather item for the city I live in by entering the values below in the query editor. You can use the name of the city you are currently in.

```
{
  "weather": "Hot",
  "town": "Pretoria"
}
```

![WeatherGQL 5.png](https://d14x58xoxfhz1s.cloudfront.net/fe71e49c-6f91-46c9-b2c5-04d134545e65)

After inputting the values for a town and weather, click `Run` and select `Mutation`. You should receive an output of a weather item created, as highlighted in the image below.

![WeatherGQL 6.png](https://d14x58xoxfhz1s.cloudfront.net/e06b2943-bb59-48d7-9bc0-bff8a45c1dc5)

- Create a few more weather items.

![WeatherGQL 7.png](https://d14x58xoxfhz1s.cloudfront.net/6de6a335-6881-427a-ae53-c30f7107aab2)

- Now go to your DynamoDB table and explore the weather items you have created.

![WeatherGQL 8.png](https://d14x58xoxfhz1s.cloudfront.net/2a6ffb24-0fa9-46c2-a4c4-ab67ff313005)

*Congratulations! You have successfully created a few weather items.*

### Lesson 3: Testing update operation

- Next, you will test the Update operation.
- Under the `mutation MyMutation`, select the `updateWeather` mutation type and check all the boxes as shown in the image below.

![WeatherGQL 9.png](https://d14x58xoxfhz1s.cloudfront.net/ad718b6d-b77b-4706-a9ac-193f0f024235)

- You will retrieve a weather item `id` from any one of the items you have created in your DynamoDB table.

![WeatherGQL 10.png](https://d14x58xoxfhz1s.cloudfront.net/aeed4798-8b07-45bc-af7e-80fe0d7bb7ea)

- Back in the AppSync console, you will input the `id` you just retrieved and make the updates you would like to make to the retrieved item.

![WeatherGQL 11.png](https://d14x58xoxfhz1s.cloudfront.net/0ed14c68-daf3-4425-b242-51d0a839aadb)

- I made an update to the weather from warm to hot. Go to your DynamoDB table and explore the weather item you have updated. Notice that the `updatedOn` field has been populated with some information and that the weather field has been updated from **Warm** to **Hot**.

![WeatherGQL 12.png](https://d14x58xoxfhz1s.cloudfront.net/def66777-0bb0-4cf2-803d-2a9e81a0f310)

- You can try and make another update like I did below.

![WeatherGQL 13 updated town name also reference when documenting.png](https://d14x58xoxfhz1s.cloudfront.net/23912049-d7e7-48d5-8f7f-e06fd1b74afb)

![WeatherGQL 14 updated town name also reference when documenting.png](https://d14x58xoxfhz1s.cloudfront.net/ee9db643-7bfb-4483-a47a-b49d5b788c59)

- *Congratulations! You have successfully updated a weather item.*

### Lesson 4: Testing the listWeathers resource

In your AppSync console, under the `query MyQuery`, select the `listWeathers` mutation type. For the `limit` input, use a value of `10`, and for the `nextToken` value, input `null`.

- Run the query.

![WeatherGQL 20 got it working.png](https://d14x58xoxfhz1s.cloudfront.net/6e888300-76e0-4b70-af3e-1e688b041681)

- Confirm that all the weather items created have been successfully retrieved from the DynamoDB table.

*Congratulations! You have successfully retrieved all the weather items you created from your DynamoDB table.*

### Lesson 5: Testing the getWeather resource

- Let's go ahead and test the GET operation.
- From your DynamoDB table, copy the `id` of an item you would like to retrieve.

![WeatherGQL 18.png](https://d14x58xoxfhz1s.cloudfront.net/ee1623c7-2576-4786-a2b4-e64cb05f11da)

- In your AppSync console, under the `query MyQuery`, select the `getWeather` mutation type and check the `id` box. Then, insert the `id` value you copied from the DynamoDB table.
- Run the query.

![WeatherGQL 19.png](https://d14x58xoxfhz1s.cloudfront.net/0a2ee7b9-1f2d-4e6a-aad8-81f8f607a31e)

- Confirm that the item you retrieved has been successfully returned from the DynamoDB table.

*Congratulations, you have successfully retrieved a weather item.*

### Lesson 6: Confirm API resources are created via the AWS console

Your API has been deployed, and you have received the endpoint URL in the outputs. Now, we confirm that our API is visible in the cloud.

- Log in to your AWS account.
- Navigate to your AWS AppSync console and select the API tab.
- Select the `WeatherGraphQLApi`. If you have created other GraphQL APIs before, you may have more than one API showing in your API tab. Make sure you select the correct API with the same endpoint URL as shown in the outputs after deployment.

![WeatherGQL 1.png](https://d14x58xoxfhz1s.cloudfront.net/8ec3b3c7-eae7-447c-8c31-1e01d4edce78)

Confirm that the DynamoDB table resource has been deployed to the cloud.

- In another tab, navigate to your DynamoDB console and select the "Tables" tab.
- Select the `WeatherTable` deployed via SAM.
- Explore the table items of your `WeatherTable` and confirm that there are no items on the table.

![WeatherGQL 2a.png](https://d14x58xoxfhz1s.cloudfront.net/5da367a9-76f0-4985-b2e1-fb988c6ff218)

![WeatherGQL 3.png](https://d14x58xoxfhz1s.cloudfront.net/e2aa2e44-6f98-46de-83f2-53ba4d9fa30d)

## Module 7: Conclusion

### Lesson 1: Conclusion

You have come to the end of the project where you have learned how to create a serverless CRUD API. You tested all the endpoints and made sure they were working. You also learned about the AWS SAM template and its anatomy and learned how to develop an API using Infrastructure as Code (IaC) tools, among other things.

## Module 8: Create resources for the Read(Get) Operation

### Lesson 1: Create a listWeathers Lambda Function Resource

In this section, you will create the resources for another READ operation for your CRUD API, which will retrieve and list all the weather items you have created.

In your `template.yaml` file, in the Resources section under your Functions resources, add the code below:

```yaml
        listWeathers:
          Runtime:
            Name: APPSYNC_JS
            Version: "1.0.0"
          DataSource: Weather
          CodeUri: ./functions/listWeathers.js 
```

The code above is no different from the other function resources you have created earlier, except for the function name and function path.

Let us explain what this function code is doing.

The `listWeathersitem` resource function resolver is fetching all the data related to all the weather items. 

It uses the **`APPSYNC_JS`** runtime and relies on the **`Weather`** data source. 

The corresponding JavaScript code is stored in the **`listWeathersItem.js`** file, which we will be creating in the next task.

Still, in your `template.yaml` file, you will create another Resource, a pipeline Resolver.

Enter the following code in the Resource section:

```yaml
           listWeathers:
            Runtime:
              Name: APPSYNC_JS
              Version: "1.0.0"
            Pipeline:
              - listWeathers
```

The code above is a resolver for a type query named `listWeathers` in the AWS AppSync API. 

Like the other resolvers you created, it uses the **`APPSYNC_JS`** runtime version 1.0.0 and employs a pipeline of a resolver function **`listWeathersItem`** to handle the mutation operation.


### Lesson 2: Create a getWeather Resolver Function

You have created the `getWeather` function resource. Now, you will need to define a function resolver for the resource you created.

Open the `functions` folder.

Rename the `getPostFromtable.js` file to `getWeather.js` and replace the code with the code below:

```jsx
import { get } from "@aws-appsync/utils/dynamodb";
export function request(ctx) {
  const key = { id: ctx.args.id };

  return get({ key: key });
}

export function response(ctx) {
  return ctx.result;
}
```

- In the **`request`** function shown in the code above, you're extracting the **`id`** from the **`ctx.args`** object and creating a **`key`** object with the **`id`**.
- Then, you call the **`get`** function with an object containing the key to retrieve an item from DynamoDB based on the specified **`id`**.
- The **`response`** function returns the result from the context **`ctx.result`**, meaning that the resolver returns the retrieved weather item from the DynamoDB table as a response.

### Lesson 3: Create a getWeather Lambda Function Resource

In this section, you will create the resources for the READ operation for your CRUD API.

In your `template.yaml` file, in the Resources section under your Functions resources, add the code below:

```yaml
        getWeatherItem:
          Runtime:
            Name: APPSYNC_JS
            Version: "1.0.0"
          DataSource: Weather
          CodeUri: ./functions/getWeatherItem.js      
```

The code above is no different from the other function resources you have created earlier, except for the function name and function path.

Let us explain what this function code is doing.

The `getWeatheritem` resource function resolver is fetching data related to a weather item. It uses the **`APPSYNC_JS`** runtime and relies on the **`Weather`** data source. The corresponding JavaScript code is stored in the **`getWeatherItem.js`** file, which we will be creating in the next task.

Still, in your `template.yaml` file, you will create another resource, a pipeline resolver.

Enter the following code in the Resource section:

```yaml
      Query:
          getWeather:
            Runtime:
              Name: APPSYNC_JS
              Version: "1.0.0"
            Pipeline:
              - getWeatherItem
```

The code above is a resolver for a type query named `deleteWeather` in the AWS AppSync API. Like the other resolvers you created, it uses the **`APPSYNC_JS`** runtime version 1.0.0 and employs a pipeline of a resolver function **`deleteWeatherItem`** to handle the mutation operation.


### Lesson 4: Create a listWeathers Resolver Function

You have created the `listWeathers` function resource. Now, you must define a resolver function for the resource you created.

Open the `functions` folder.

Create a new file called `listWeathers.js` and copy and paste the code below:

```jsx
import { scan } from "@aws-appsync/utils/dynamodb";
export function request(ctx) {
  const { limit = 10, nextToken } = ctx.args;

  return scan({ limit, nextToken });
}

export function response(ctx) {
  return ctx.result.items;
}
```

- In the **`request`** function above, you are extracting the **`limit`** and **`nextToken`** from the **`ctx.args`** object.

- The **`limit`** specifies the maximum number of items to scan, with a default value of 10, and **`nextToken`** is used for pagination.

- You then call the **`scan`** function with these parameters to perform a scan operation on the DynamoDB table.

- The **`response`** function returns the items obtained from the scan operation, which means that the resolver returns all the weather items from the DynamoDB table as a response.


## Module 9: Introduction

### Lesson 1: Prerequisites

Before proceeding, please make sure you have the below technologies installed and configured properly. Please check out our Prerequisites course for guidelines on how to configure the prerequisites for this course.

1. [AWS Account](https://aws.amazon.com/): We'll be deploying the application to the AWS Cloud in order to test and confirm its functionalities.
2. [AWS Command Line Interface (AWS CLI)](https://awscli.amazonaws.com/AWSCLIV2.msi). The AWS CLI provides direct access to the public APIs of AWS services. You can explore a service's capabilities with the AWS CLI, and develop shell scripts to manage your resources
3. [AWS SAM CLI](https://github.com/aws/aws-sam-cli/releases/latest/download/AWS_SAM_CLI_64_PY3.msi). AWS Serverless Application Model Command Line Interface, provides a Lambda-like execution environment that lets you locally build, test, and debug applications defined by SAM templates or through the AWS Cloud Development Kit (CDK)
4. [Node.js](https://nodejs.org/en)

The AWS Toolkit is an open source plug-in for popular IDEs that uses the SAM CLI to build and deploy serverless applications on AWS.

The AWS Toolkit also adds a simplified step-through debugging experience for Lambda function code.

See the following links to get started

- [VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)
- [Visual Studio](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/welcome.html)

### Lesson 2: Services and technologies

### AWS Serverless Application Model (SAM)

The AWS Serverless Application Model (SAM) is an open-source framework for building serverless applications. It provides shorthand syntax to express functions, APIs, databases, and event source mappings. With just a few lines per resource, you can define the application you want and model it using YAML. There is no additional charge to use AWS SAM. You pay for the AWS resources created using SAM in the same manner as if you had created them manually. You only pay for what you use as you use it. There are no minimum fees and no required upfront commitments.

### **AWS AppSync**

AWS AppSync is a fully managed service that makes it easy to develop GraphQL APIs by handling the heavy lifting of securely connecting to data sources like Amazon DynamoDB, AWS Lambda, and more. With AppSync, you can build scalable applications with real-time and offline capabilities. It simplifies the process of building data-driven applications by automatically generating GraphQL APIs based on your defined schema and resolvers. AppSync also provides features like data synchronization, conflict resolution, and caching to improve performance and reliability.

### JavaScript Resolvers

[Resolvers](https://docs.aws.amazon.com/appsync/latest/devguide/resolver-reference-overview-js.html) are the connectors between GraphQL and a data source. They tell AWS AppSync how to translate an incoming GraphQL request into instructions for your backend data source and how to translate the response from that data source back into a GraphQL response.

## Module 10: Define the schema

### Lesson 1: Create a GraphQL Schema

- From your project root, create a new folder called `schema` and move the `schema.graphql` file to that folder.
- Go to the `schema.graphql` file and replace the existing code with the following:

```graphql
schema {
  query: Query
  mutation: Mutation
}

type Query {
  getWeather(id: String!): Weather!
  listWeathers(limit: Int, nextToken: String): [Weather!]!
}

type Mutation {
  createWeather(weather: String!, town: String!): Weather!
  updateWeather(id: String!, weather: String, town: String!): Weather!
  deleteWeather(id: String!): Boolean!
}

type Weather {
  id: String!
  weather: String!
  town: String!
  createdOn: AWSTimestamp!
  updatedOn: AWSTimestamp
}
```

Let’s break down the above code:

- Your GraphQL schema specifies two root types: **`query`** and **`mutation`**. The **`query`** type is used for read operations, and the **`mutation`** type is used for write operations.

**The query types:**

- **`getWeather`**: Takes an **`id`** argument and returns a single **`Weather`** object.
- **`listWeathers`**: Takes optional **`limit`** and **`nextToken`** arguments, and returns a list of **`Weather`** objects.

**The mutation type:**

- **`createWeather`**: Takes **`weather`** and **`town`** arguments and creates a new **`Weather`** object.
- **`updateWeather`**: Takes **`id`**, **`weather`**, and **`town`** arguments and updates an existing **`Weather`** object.
- **`deleteWeather`**: Takes an **`id`** argument and returns a boolean indicating the success of the deletion

**The weather types:**

- **`id`**: Unique identifier for a weather entry.
- **`weather`**: String representing the weather.
- **`town`**: String representing the town associated with the weather.
- **`createdOn`**: AWS Timestamp indicating when the weather entry was created.
- **`updatedOn`**: AWS Timestamp indicating when the weather entry was last updated.

## Module 11: Deployment

### Lesson 1: Deploy the SAM stack

To test our API, we first need to deploy it to the cloud.

Please download the complete code from the download section and let's proceed to deployment  by running the following commands:

```
sam build
sam deploy --guided
```

Follow the prompts as you did in [Module 1](https://www.notion.so/Project-Setup-cae8a4c9b7a942f9aa09f878872ead8a?pvs=21) and select "yes" to deploy the changeset.

You should see your WeatherGraphQLApi endpoint URL and the API Key for WeatherGraphQLApi in your `Outputs`.

Congratulations, you have successfully deployed your GraphQL API. Proceed to the next module where you will test your CRUD operations for your application.

