# Apartment Complex Management System

## Overview
This course will teach you how to build a graphql api for an apartment complex management system using AWS Serverless Technology.

You will learn how to use 
- AWS Lambda, 
- Amazon Cognito, 
- Amazon DynamoDB, 
- Amazon SQS
- and AWS AppSync to create a scalable, secure, and cost-effective system for managing your apartment complex.


## Course Objectives

By the end of this course, you will be able to:

- Understand the benefits of using AWS Serverless Technology to build scalable GraphQL APIs.
- Design and implement an AWS Serverless Technology solution.
- Use AWS Lambda to create serverless functions for handling common tasks.
- Use Amazon SQS for queueing and decoupling applications.
- Use Amazon Cognito to authenticate and authorize users.
- Use Amazon DynamoDB to store data about your apartment complex



## Solutions Architecture

![alt text](https://d14x58xoxfhz1s.cloudfront.net/724ec14b-3495-48f9-bb74-006c0267dff4)

## Description
This course will teach you how to build a graphql api for an apartment complex management system using AWS Serverless Technology.

You will learn how to use

AWS Lambda,
Amazon Cognito,
Amazon DynamoDB,
Amazon SQS
and AWS AppSync to create a scalable, secure, and cost-effective system for managing your apartment complex.

## Course Details
- **Number of Modules:** 3
- **Image:** https://d14x58xoxfhz1s.cloudfront.net/c889bfb8-d923-4dbf-a1c5-bcba86d0fcc0
- **Difficulty:** Advanced
- **Framework:** AWS CDK
- **Programming_language:** Python
- **Web_framework:** React,VueJs
- **Mobile_framework:** Flutter
- **ServerlessTopic:** serverless_architecture,event_driven_architecture
- **MainCourse:** true
- **MainCourseId:** N/A
- **Trailer:** 
- **Video:** N/A
- **File:** N/A
- **CodeVisible:** false
- **UploadVisible:** false
- **Tasks:** false
- **Publish:** true
- **ProposedCourses:** N/A
- **AuthorId:** 3c926a9e-9406-45e2-98d9-006600258387
- **AuthorGroup:** admin
- **Duration:** 5h:30m
- **Featured:** N/A
- **DefaultMedia:** N/A
- **NumberOfLessons:** 19
- **CreatedAt:** 2023-06-11T09:17:49.483Z
- **UpdatedAt:** 2024-10-12T04:30:45.843Z
- **CourseCategoryCourseId:** ac49bd8c-68fe-45c4-8b6a-37bf9ee28389
- **_version:** 21
- **_lastChangedAt:** 1728707445881
- **_deleted:** N/A

## Module 1: Testing

### Lesson 1: Testing the create user account endpoint

## Testing CreateUserAccount

```graphql
createUserAccount(input: UserInput!): User! @aws_cognito_user_pools
```

We’ll be doing tests from the Appsync console. Sign into your AWS console and navigate to you AppSync. Click on your project name form the Appsync console, once the project is open, navigate to Queries on the left hand-side menu of the screen.

![alt text](https://d14x58xoxfhz1s.cloudfront.net/bd68e134-f4ae-47d9-a1b0-83bf0a8700ea)

Let’s create a user account, using the `createUserAccount` mutation and an `apikey`. 

You’ll get the error `Not Authorized to access createUserAccount on type Mutation`.That’s because we added the directive `@aws_cognito_user_pool` , which requires a user to be signed in, before accessing that endpoint. 

Therefore, we need to create a new user in Cognito and then use that user to access the endpoints in our API.

From the aws console search bar, type cognito and open up the cognito user pools page.

Navigate to your project and create a new user.

![alt text](https://d14x58xoxfhz1s.cloudfront.net/1ca3354a-a428-4422-a2e2-1417de7a542d)


Once created, go back to your project on Appsync and sign in with the username and password you just created.

![alt text](https://d14x58xoxfhz1s.cloudfront.net/47b08fcf-562c-42b7-81cb-6e5889721272)

![alt text](https://d14x58xoxfhz1s.cloudfront.net/63104fcb-ad1e-4644-be89-b20522eefa23)

Once logged in, run the endpoint again. If everything goes smoothly, you’ll see a result similar to this, based on the inputs you gave.

![alt text](https://d14x58xoxfhz1s.cloudfront.net/8be58e55-d96b-40ad-a8ef-d19a6c6cf9fe)

### Lesson 2: Conclusion

## Conclusion
And that's it for this course.

The Complete working code is on [github](https://github.com/trey-rosius/apartment_complex_management_system)


### Lesson 3: Testing create apartment booking endpoint

### Testing `createApartmentBooking` Endpoint

Sign in to your appsync account on the aws console, navigate to your project and run the following mutation.

```graphql
mutation create {
createApartmentBooking(input: {apartmentId: "2F6hDMkdfeX4wQau7Bhoi7cOuAH",
 bookingStatus: PENDING, endDate: "2022-10-22", startDate: "2022-09-22", 
userId: "[test1@gmail.com](mailto:test1@gmail.com)"})
}
```

Change the values of the `apartmentId` and `userId` to match those in your dynamoDB table.

If the mutation runs successfully, a `true` is returned.


![alt text](https://d14x58xoxfhz1s.cloudfront.net/31c09ff0-db35-4f89-a149-a3a5e805ea15)

If we go to `processSqsBooking` lambda and look at its logs, we see that it has received a message. 

![alt text](https://d14x58xoxfhz1s.cloudfront.net/5084a625-44d9-4d27-a676-9d19ee0953b0)

Then, the lambda would save this message into dynamoDB.

![alt text](https://d14x58xoxfhz1s.cloudfront.net/dd0a386c-02be-4a87-8c80-7e5f06e6d714)

If you attempt to run the mutation again with same values for `userId` and `apartmentId`, meaning that the same user wants to book the same apartment, with a previous `PENDING` booking status already in the system, the mutation fails.

`You already have a pending booking for this apartment`

![alt text](https://d14x58xoxfhz1s.cloudfront.net/7a7e98d9-57ae-4112-b5cc-97d8c12f68e6)

Please create multiple users and create bookings with each of those users. We’ll be needing them in the next step.

After creating multiple bookings for an apartment, we want to give the building owner(Admin), a way to retrieve all bookings for each of their apartments, in-order to `APPROVE` or `DENY` a booking.

### Lesson 4: Testing get all bookings per apartment endpoint

## Testing `getAllBookingsPerApartment` endpoint.

Open up your appsync app in the aws console and run the query `getAllBookingsPerApartment`.Make sure you use an `apartmentId` for an apartment that has multiple booking.

![alt text](https://d14x58xoxfhz1s.cloudfront.net/b1a8c1b6-1572-4956-bf1c-006300a6a81f)


```tsx
{
  "data": {
    "getAllBookingsPerApartment": [
      {
        "apartmentId": "2FGKLMWeMiCJeMZH9OqxEFR0sgh",
        "bookingStatus": "PENDING",
        "endDate": "2022-10-22",
        "id": "2FGKty2bIUaLr0C4Hc513rkX5oT",
        "startDate": "2022-09-22",
        "userId": "treyrosius@gmail.com",
        "user": {
          "email": "treyrosius@gmail.com",
          "firstName": "Rosius",
          "id": "2FGJzw5eiS5pWDUwH9r1PkjROYV",
          "lastName": "Ndimofor Ateh",
          "userType": "ADMIN",
          "verified": true
        }
      },
      {
        "apartmentId": "2FGKLMWeMiCJeMZH9OqxEFR0sgh",
        "bookingStatus": "PENDING",
        "endDate": "2022-10-22",
        "id": "2FGVn4SwbXF8LUsID3tY9lWTziO",
        "startDate": "2022-09-22",
        "userId": "test@gmail.com",
        "user": {
          "email": "test@gmail.com",
          "firstName": "Steve",
          "id": "2FGK3F4WKV28Y9edwsgUjn9gIuG",
          "lastName": "Rosius",
          "userType": "ADMIN",
          "verified": true
        }
      },
      {
        "apartmentId": "2FGKLMWeMiCJeMZH9OqxEFR0sgh",
        "bookingStatus": "PENDING",
        "endDate": "2022-10-22",
        "id": "2FGVr0WV3cqyIJSqOQc7kN4HwFg",
        "startDate": "2022-09-22",
        "userId": "tony@gmail.com",
        "user": {
          "email": "tony@gmail.com",
          "firstName": "Stark",
          "id": "2FGK8BOvlQMDWcQarYtTR2RAQ7a",
          "lastName": "Tony",
          "userType": "TENANT",
          "verified": true
        }
      }
    ]
  }
}
```

Notice that each booking as a user object. We don’t have to make an api request to get the `user` object separately.

### Lesson 5: Testing the create building endpoint

### Testing the createBuilding Endpoint

```tsx
createBuilding(input: BuildingInput!): Building!
    @aws_cognito_user_pools(cognito_groups: ["Admins"])
```

This endpoint is only accessible to users belonging the the group `Admins` .

So the first step is to go to your project in Cognito, create a group called `Admins` and add the user you created above to that group.

![alt text](https://d14x58xoxfhz1s.cloudfront.net/0b84296e-765e-4b86-b4dc-e56fd91d843a)

Navigate back to your Appsync project, fill in the endpoints input and run it. If everything goes smoothly, you should see this, based on the input you added.


![alt text](https://d14x58xoxfhz1s.cloudfront.net/1ffd7ea8-ed5e-4b57-9941-dda50355a182)

## Module 2: Introduction

### Lesson 1: Get started

## GET STARTED

### Initialize CDK app

Firstly, create a new project folder. I’m using a mac, so i’ll create a folder called `acms` and cd into it

`mkdir acms`

`cd acms`

Next, initialize a CDK typescript application in your newly created folder.

`cdk init --language typescript`

Once created, open up the CDK app in your favorite IDE.

### Dependencies

Add these dependencies to the `package.json` file in the cdk project. 

```jsx
"@aws-lambda-powertools/logger": "^0.9.1",
"@aws-lambda-powertools/tracer": "^0.9.1",
"@types/aws-lambda": "^8.10.101",
"aws-sdk": "^2.1153.0",
"ksuid": "^2.0.0",
```

We’ll be using the `lambda-powertools` typescript library for logging and tracing. 

Feel free to read more about the library here [https://awslabs.github.io/aws-lambda-powertools-typescript/latest/](https://awslabs.github.io/aws-lambda-powertools-typescript/latest/)

`ksuid` stands for K-Sortable Unique Identifier. Its an efficient, comprehensive, battle-tested Go library for generating and parsing a specific kind of globally unique identifier called a *KSUID.*

Learn more about the library here [https://github.com/segmentio/ksuid](https://github.com/segmentio/ksuid)

### Lesson 2: Solutions architecture

## Solutions Architecture

![alt text](https://d14x58xoxfhz1s.cloudfront.net/724ec14b-3495-48f9-bb74-006c0267dff4)

## ERD(Entity Relationship Diagram)

### Entities

- Buildings(A building has many apartments)
- Apartments(Apartments are in buildings)
- Bookings(Each apartment can have multiple pending bookings. Once a booking has been approved, payment can be made. )
- Notifications(Light, Water, internet bills due)
- Payments(Before payment, booking status equals Approved. After payment, booking status equals PAID )
- Users(Administrators,CareTakers, Tenants)

### Relationships between entities

Buildings and Apartments share a one to many relationship(one building can have multiple apartments)

Apartments and Bookings share a one to many relationship(One Apartment can have multiple bookings. Whoever pays first gets in)

Users and Apartments share a one to many relationship(One user can have multiple apartments)

Users and Bookings share a one to many relationship(One user can create multiple bookings)

Users and Payments share a one to many relationship

![alt text](https://d14x58xoxfhz1s.cloudfront.net/4f66075e-64b2-4de8-8897-e6f5455c346d)

### Lesson 3: Introduction


# Welcome to the Apartment Complex Management System(ACMS) Serverless Application

## Concept

In this course, we'll use Serverless to build a system where Building owners can:

- Create personal accounts.
- Register the buildings(name, address, number of apartments etc) they own.
- Assign and keep Caretakers to manage each of those buildings.
- Keep track of the tenants occupying the apartments in the building.
- Keep track of occupied and vacant apartments, bookings,payments, and a lot more in each of their building.
- And other useful information that’ll provide more insights on the management of their buildings.

We'll build and deploy a serverless GraphQL API with Appsync,Cdk and Typescript.

## Prerequisites

Install these dependencies before proceeding.

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
- [AWS ACCOUNT AND USER](https://cdkworkshop.com/15-prerequisites/200-account.html)
- [Node Js](https://cdkworkshop.com/15-prerequisites/300-nodejs.html)
- [AWS CDK ToolKit](https://cdkworkshop.com/15-prerequisites/500-toolkit.html)
- [AWS AppSync](https://aws.amazon.com/appsync/) is a fully managed serverless service that makes it easy to develop GraphQL APIs in the cloud. It handles the heavy lifting of managing a complex GraphQL backend infrastructure, securely connecting to data sources, adding caches to improve performance, subscriptions to support real-time updates, and client-side data stores that keep offline clients in sync.
- GraphQL provides a flexible typed data query language for APIs as well as a runtime to fulfill these queries
- The [AWS Cloud Development Kit (AWS CDK)](https://aws.amazon.com/cdk/) is an open-source software development framework to define your cloud application resources using familiar programming languages

### Lesson 4: Access patterns

# Access Patterns

Administrator

- Create/update/delete Administrator accounts.

```jsx
PK:USER#EMAIL
SK:USER#EMAIL
```

- Create/Update/Read/List/Delete Buildings

```jsx
PK:BUILDING
SK:BUILDING#BUILDINGID
```

- Create/Update/Delete Apartments

```jsx
PK:BUILDING#BUILDINGID
SK:APARTMENT#APARTMENTID
```

- list all buildings

```jsx
starts_with(BUILDING#)
PK:BUILDING
SK: BUILDING#
```

- list apartments per building

```jsx
starts_with(APARTMENT#)
PK:BUILDING#BUILDINGID
SK:APARTMENT#
```

- list all bookings per apartment

```jsx
begins_with(BOOKINGS#)
PK:APARTMENTS#APARTMENTID
SK:BOOKINGS#
```

Tenants

- Create/update/read/delete account

```jsx
PK:USER#EMAIL
SK:USER#EMAIL

```

- List all Buildings in their Area

```jsx
filter with `longitude` and `latitude`
PK:BUILDING
SK:BUILDING#BUILDINGID
```

- List available apartments for each building

```jsx
conditional expression `where status==available`
PK:BUILDING#BUILDINGID
SK:APARTMENT#
```

- Book an apartment

```jsx

BOOKING_STATUS = PENDING

PK:USER#USERNAME
SK:APARTMENT#APARTMENTID
GSI
GSI1PK:BUILDING#BUILDINGID
GSI1SK:APARTMENT#APARTMENTID#STATUS
```

### Single Table DynamoDB Design



![alt text](https://d14x58xoxfhz1s.cloudfront.net/c3fd05c6-cdf3-4109-bc5c-3195182963eb)


## NOSQL WORKBENCH

![alt text](https://d14x58xoxfhz1s.cloudfront.net/4b71d8ca-5dc9-44da-813c-254b7c2a0ee6)

### Get All Apartments Per Building

![alt text](https://d14x58xoxfhz1s.cloudfront.net/fb514f53-ce05-498f-b441-8516311df909)

### Get All Bookings Per Apartment

![alt text](https://d14x58xoxfhz1s.cloudfront.net/fd2f5bc9-9096-476c-b740-010b857f69a2)


### Get All Buildings Per User

![alt text](https://d14x58xoxfhz1s.cloudfront.net/e1b30692-39b0-4cea-a162-0478d6a4ec64)


## Module 3: Building the api

### Lesson 1: Building stack

## Building Stack

The building stack follows the same process of creation like the user stack.

Here’s the building endpoint we will be creating.

```tsx
createBuilding(input: BuildingInput!): Building!
    @aws_cognito_user_pools(cognito_groups: ["Admins"])
```

A building can only be created by 

- A logged in User
- The User has to belong to the `Admins` group.

Inside the `lib` folder, create a file named `building-lambda-stack.ts`.

We will be needed the `CfnGraphQLApi` , the `CfnGraphQLSchema` and `Table` same as `user` stack.

At the top of the `building-lambda-stack.ts` file, create an interface which extends `StackProps` and define the 3 resources we intend importing from the main stack.

```tsx
interface BuildingLambdaStackProps extends StackProps {
  acmsGraphqlApi: CfnGraphQLApi;
  apiSchema: CfnGraphQLSchema;
  acmsDatabase: Table;
}
```

Then the Building stack looks like this 

```tsx
export class BuildingLamdaStacks extends Stack {
  constructor(scope: Construct, id: string, props: BuildingLambdaStackProps) {
    super(scope, id, props);

    const { acmsDatabase, acmsGraphqlApi, apiSchema } = props;
}
}
```

Let’s go ahead and define our lambda, resolver and datasource.

Create a folder called `building` inside `lib/lambda-fns`.Inside the `building` folder, create a folder called entities, which would contain the building entity. 

Create a filed named `app.ts` that’ll serve as the lambda handler for building endpoints.

Open up the `building-lambda-stacks.ts` file and define the rest of the resources like so.

### Lambda

```tsx
const buildingLambda = new NodejsFunction(this, "AcmsBuildingHandler", {
      tracing: Tracing.ACTIVE,
      codeSigningConfig,
      runtime: lambda.Runtime.NODEJS_16_X,
      handler: "handler",
      entry: path.join(__dirname, "lambda-fns/building", "app.ts"),

      memorySize: 1024,
    });
```

### Lambda Datasource

```tsx
const lambdaDataSources: CfnDataSource = new CfnDataSource(
      this,
      "ACMSBuildingLambdaDatasource",
      {
        apiId: acmsGraphqlApi.attrApiId,
        name: "ACMSBuildingLambdaDatasource",
        type: "AWS_LAMBDA",

        lambdaConfig: {
          lambdaFunctionArn: buildingLambda.functionArn,
        },
        serviceRoleArn: appsyncLambdaRole.roleArn,
      }
    );
```

### Resolver

```tsx
const createBuildingResolver: CfnResolver = new CfnResolver(
      this,
      "createBuildingResolver",
      {
        apiId: acmsGraphqlApi.attrApiId,
        typeName: "Mutation",
        fieldName: "createBuilding",
        dataSourceName: lambdaDataSources.attrName,
      }
    );
```

Grab the complete code for `building-lambda-stack.ts` here. [https://github.com/trey-rosius/apartment_complex_management_system/blob/master/lib/building-lambda-stack.ts](https://github.com/trey-rosius/apartment_complex_management_system/blob/master/lib/building-lambda-stack.ts)

Next step is to implement endpoint routing logic in the buildings lambda handler `app.ts.`

Firstly, here’s the input schema for the `createBuilding` endpoint.

```graphql
input BuildingInput {
  name: String!
  userId: String!
  numberOfApartments: Int!
  address: AddressInput!
}
```

Here’s how the `app.ts` file looks like

```tsx
const logger = new Logger({ serviceName: "ApartmentComplexManagementApp" });

type BuildingInput = {
  name: string;
  userId: string;
  numberOfApartments: number;
  address: {
    streetAddress: string;
    postalCode: string;
    city: string;
    country: string;
  };
};

exports.handler = async (
  event: AppSyncResolverEvent<BuildingInput>,
  context: Context
) => {
  logger.addContext(context);
  logger.info(
    `appsync event arguments ${event.arguments} and event info ${event.info}`
  );
  switch (event.info.fieldName) {
    case "createBuilding":
      return await createBuilding(event.arguments, logger);

    default:
      return null;
  }
};
```

Create a file called `createBuilding.ts` inside `lib\lambda-fns\building\` .

This file would contain code for the  `createBuilding` function, that performs a put request on the DynamoDB table, based on the input.

```tsx
async function createBuilding(buildingInput: BuildingInput, logger: Logger) {
  const documentClient = new DynamoDB.DocumentClient();
  let tableName = process.env.ACMS_DB;
  const createdOn = Date.now().toString();
  const id: string = uuid();
  if (tableName === undefined) {
    logger.error(`Couldn't get the table name`);
    tableName = "AcmsDynamoDBTable";
  }

  const input: BuildingEntity = new BuildingEntity({
    id: id,
    ...buildingInput,
    createdOn,
  });

  logger.info(`create building input info", ${buildingInput}`);
  const params = {
    TableName: tableName,
    Item: input.toItem(),
  };

  try {
    await documentClient.put(params).promise();
    return input.graphQlReturn();
  } catch (error: any) {
    logger.error(`an error occured while creating a building ${error}`);
    throw Error(`an error occured ${error}`);
  }
}
```

Don’t forget to add the building stack to your app like so

```tsx
const app = new cdk.App();
const acmsStack = new AcmsStack(app, "AcmsStack", {
  env: { account: "13xxxxxxxxxx", region: "us-east-2" },

  /* For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html */
});

new UserLamdaStacks(app, "UserLambdaStacks", {
  env: { account: "13xxxxxxxxxx", region: "us-east-2" },
  acmsDatabase: acmsStack.acmsDatabase,
  apiSchema: acmsStack.apiSchema,
  acmsGraphqlApi: acmsStack.acmsGraphqlApi,
});

new BuildingLamdaStacks(app, "BuildingLambdaStacks", {
  env: { account: "13xxxxxxxxxx5", region: "us-east-2" },
  acmsDatabase: acmsStack.acmsDatabase,
  apiSchema: acmsStack.apiSchema,
  acmsGraphqlApi: acmsStack.acmsGraphqlApi,
});
```

### Lesson 2: Bookings stack

### Bookings stack

The booking stack is interesting. Let’s take a look at the booking architecture again.


![alt text](https://d14x58xoxfhz1s.cloudfront.net/c9cf0d4e-b207-4116-8265-7cbd2034ea1e)

So basically, when a user creates a booking, a message containing the booking details is bundled up by a lambda and sent to an SQS Queue. 

Another lambda function polls the messages from SQS and saves them into a dynamoDb table.

If a message can’t be processed, it is sent to a Dead Letter Queue(DLQ). Once in DLQ, the message can be reviewed and deleted or reprocessed if need be.

We used SQS here in-order to: 

- Decouple the app and make it more scalable.
- Not loose any bookings when too many requests are made at same time.

Back to the IDE. Let’s go ahead and create the necessary files and folders that’ll contain the code for this stack.

Inside `lib` folder, create a file called `booking-lamda-stack.ts` to define resources related to the booking stack.Then inside `lib\lambda-fns` , create a folder called `booking`. 

Inside the `booking` folder, create these :

1. `app.ts` 
2. `createApartmentBooking.ts`
3. `confirmBooking.ts`
4. `CreateBookingInput.ts`
5. `processSqsBooking.ts`

Then create this folder:

- `entities`

Here’s how the directory structure for the booking stack looks like

![alt text](https://d14x58xoxfhz1s.cloudfront.net/be3d6f4e-c89c-4274-8828-d73a10fb9f68)

The `booking-lambda-stack.ts` contains 2 lambdas.

The first lambda `CreateApartmentBooking.ts` acts as the lambda resolver for the appsync endpoint `createApartmentBooking`.

This lambda function takes the below input, bundles it up and sends it to an SQS queue.

Before sending to SQS , the function first checks  to see if this particular user has a `PENDING`  booking status for this apartment. 

If a user’s booking status for an apartment is  `PENDING` , they can’t make subsequent bookings for same apartment.

The second lambda function `processSqsBooking.ts` polls for bookings(messages) in the queue and saves them to dynamoDB.

In this fashion, we have completely decoupled the application, making it more scalable and performant, by taking booking processing, off the main thread.

```graphql
input CreateBookingInput {
  userId: String!
  apartmentId: String!
  startDate: AWSDate!
  endDate: AWSDate!
  bookingStatus: BookingStatus!
}
enum BookingStatus {
  PENDING
  APPROVED
  CANCELLED
}
```

Let’s get started.

We’ll create the SQS queue and assign a Dead Letter Queue(DLQ) to it with a `maxReceiveCount` of 10. Open `booking-lambda-stack.ts` and type in the following code.

```tsx
const dlq = new sqs.Queue(this, "DeadLetterQueue");
    const queue = new sqs.Queue(this, "bookingQueue", {
      deadLetterQueue: {
        queue: dlq,
        maxReceiveCount: 10,
      },
    });
```

Now, let’s add the 2 functions

```tsx
/**
     * booking function
     */
    const bookingLambda: NodejsFunction = new NodejsFunction(
      this,
      "AcmsBookingHandler",
      {
        tracing: Tracing.ACTIVE,
        codeSigningConfig,
        runtime: lambda.Runtime.NODEJS_16_X,
        handler: "handler",
        entry: path.join(__dirname, "lambda-fns/booking", "app.ts"),
        initialPolicy: [policyStatement],
        role: lambdaRole,

        memorySize: 1024,
      }
    );

    /**
     * Process SQS Messages Lambda
     */
    const processSQSLambda: NodejsFunction = new NodejsFunction(
      this,
      "ProcessSqSBookingHandler",
      {
        tracing: Tracing.ACTIVE,
        codeSigningConfig,
        runtime: lambda.Runtime.NODEJS_16_X,
        handler: "handler",
        entry: path.join(
          __dirname,
          "lambda-fns/booking",
          "processSqsBooking.ts"
        ),
        initialPolicy: [policyStatement],
        role: lambdaQueueRole,

        memorySize: 1024,
      }
    );
```

Let’s attach the SQS consuming lambda(processSQSLambda) function to and SQS event source

```tsx
/**
     * lambda to sqs
     */

    const eventSourceMapping = new lambda.EventSourceMapping(
      this,
      "QueueConsumerFunctionBookingEvent",
      {
        target: processSQSLambda,
        batchSize: 10,
        eventSourceArn: queue.queueArn,
        reportBatchItemFailures: true,
      }
    );
```

Don’t forget the datasource and the resolver

```tsx
const lambdaDataSources: CfnDataSource = new CfnDataSource(
      this,
      "ACMSBookingLambdaDatasource",
      {
        apiId: acmsGraphqlApi.attrApiId,
        name: "ACMSBookingLambdaDatasource",
        type: "AWS_LAMBDA",

        lambdaConfig: {
          lambdaFunctionArn: bookingLambda.functionArn,
        },
        serviceRoleArn: appsyncLambdaRole.roleArn,
      }
    );

    const createApartmentBookingResolver: CfnResolver = new CfnResolver(
      this,
      "createApartmentBookingResolver",
      {
        apiId: acmsGraphqlApi.attrApiId,
        typeName: "Mutation",
        fieldName: "createApartmentBooking",
        dataSourceName: lambdaDataSources.attrName,
      }
    );
```

Then permissions and environment variables

```tsx
    createApartmentBookingResolver.addDependsOn(apiSchema);
    getResultBookingPerApartmentResolver.addDependsOn(apiSchema);
    acmsDatabase.grantReadData(processSQSLambda);
    acmsDatabase.grantReadData(bookingLambda);
    queue.grantSendMessages(bookingLambda);
    queue.grantConsumeMessages(processSQSLambda);
    bookingLambda.addEnvironment("ACMS_DB", acmsDatabase.tableName);
    bookingLambda.addEnvironment("BOOKING_QUEUE_URL", queue.queueUrl);
```

Grab the complete code for this file [here]([https://github.com/trey-rosius/apartment_complex_management_system/blob/master/lib/booking-lambda-stack.ts](https://github.com/trey-rosius/apartment_complex_management_system/blob/master/lib/booking-lambda-stack.ts))

### `CreateApartmentBooking.ts`

As we mentioned earlier, we need to first check for any PENDING bookings by this particular user and the apartment.

We use a Global Secondary Index called `getAllApartmentsPerUser` and a filter to get all PENDING  apartment bookings for this user.

```tsx
const params = {
    TableName: tableName,
    IndexName: "getAllApartmentsPerUser",
    KeyConditionExpression: "#GSI1PK = :GSI1PK AND #GSI1SK = :GSI1SK",
    FilterExpression: "#bookingStatus = :bookingStatus",
    ExpressionAttributeNames: {
      "#GSI1PK": "GSI1PK",
      "#GSI1SK": "GSI1SK",
      "#bookingStatus": "bookingStatus",
    },
    ExpressionAttributeValues: {
      ":GSI1PK": `USER#${appsyncInput.input.userId}`,
      ":GSI1SK": `APARTMENT#${appsyncInput.input.apartmentId}`,
      ":bookingStatus": "PENDING",
    },
  };

  //We want to make sure this particular user doesn't already have a pending booking for this apartment.
  const response = await documentClient.query(params).promise();
```

And then, we proceed, based on the response of the query.

```tsx
if (response.Count != null) {
    //No pending booking, send booking to SQS

    if (response.Count <= 0) {
      logger.info(`sqs pre message ${JSON.stringify(bookingInput.toItem())}`);
      logger.info(`sqs  queue url ${BOOKING_QUEUE_URL}`);
      var sqsParams: SQS.Types.SendMessageRequest = {
        MessageBody: JSON.stringify(bookingInput.toItem()),
        QueueUrl: BOOKING_QUEUE_URL,
      };

      try {
        await sqs.sendMessage(sqsParams).promise();
        return true;
      } catch (error) {
        logger.info(`an error occured while sending message to sqs", ${error}`);
        throw Error(`an error occured while sending message to sqs", ${error}`);
      }
    }
    //Pending Booking,don't send any message to SQS
    else {
      throw new Error("You Already have a pending booking for this apartment");
    }
  } else {
    throw new Error("Error Querying pending bookings");
  }
```

### Lesson 3: User stack

## User Stack

In this stack, we’ll define all resources related to the user entity.

We have 3 user related endpoints defined in the `schema.graphql` file.

But we will implement  `createUserAccount` endpoint only.

```graphql
createUserAccount(input: UserInput!): User! @aws_cognito_user_pools
updateUserAccount(input: UpdateUserInput!): User! @aws_cognito_user_pools
deleteUserAccount(id: ID!): Boolean! @aws_cognito_user_pools
```

Create a file called `user-lambda-stack.ts` in the `lib` folder. 

Remember that, when we created the main stack above, we made a couple of resources public, meaning they could be shared and used within stacks.

`

```
  public readonly acmsDatabase: Table;
  public readonly acmsGraphqlApi: CfnGraphQLApi;
  public readonly apiSchema: CfnGraphQLSchema;
  public readonly acmsTableDatasource: CfnDataSource;
```

In the User stack, we will be needed the `CfnGraphQLApi` , the `CfnGraphQLSchema` and `Table`

At the top of the `user-lambda-stack.ts` file, create an interface which extends `StackProps` and define the 3 resources we intend importing from the main stack.

```jsx
interface UserLambdaStackProps extends StackProps {
  acmsGraphqlApi: CfnGraphQLApi;
  apiSchema: CfnGraphQLSchema;
  acmsDatabase: Table;
}
```

Then, in the constructor for class `UserLambdaStacks`, change `StackProps` to `UserLambdaStackProps`.

So now, here’s how the `user-lambda-stack` looks like 

```jsx
interface UserLambdaStackProps extends StackProps {
  acmsGraphqlApi: CfnGraphQLApi;
  apiSchema: CfnGraphQLSchema;
  acmsDatabase: Table;
}
export class UserLamdaStacks extends Stack {
  constructor(scope: Construct, id: string, props: UserLambdaStackProps) {
    super(scope, id, props);

    const { acmsDatabase, acmsGraphqlApi, apiSchema } = props;

}
}
```

Notice that we’ve also de-structured the `props` to get all the resources defined in the interface.

We are going to be using a lambda resolver to resolve all endpoints for this user entity.

Let’s go ahead and get started

### Lesson 4: Stacks

### Stacks

We are going to have 6 stacks in total.

- The main application Stack(Defines the Appsync API, Database, Datasource etc. for the complete app)
- A User Stack (For User Resources)
- A Building Stack (For Building Resources)
- An Apartment Stack (For Apartment Resources)
- A Bookings Stack (For Booking Resources)
- DynamoDb Stream Stack

To provision infrastructure resources, all constructs that represent AWS resources must be defined, directly or indirectly, within the scope of a Stack construct.

An App is a container for one or more stacks: it serves as each stack’s scope. Stacks within a single App can easily refer to each other's resources (and attributes of those resources).

The AWS CDK infers dependencies between stacks so that they can be deployed in the correct order. You can deploy any or all of the stacks defined within an app with a single cdk deploy command.

Our app is defined in the `bin` folder, while our stacks are in the `lib` folder.

Add your `account` and `region` to the `env` object in the cdk app file located in the `bin` folder.

Here’s how mine looks like

```
const app = new cdk.App();const acmsStack = new AcmsStack(app, "AcmsStack", {  env: { account: "13xxxxxxxxxx", region: "us-east-2" },});
```

`AcmsStack` file is located the `lib` folder.

### Lesson 5: Get all bookings per apartment

### Get All Bookings Per Apartment

In-order for an admin to approve a booking for an apartment, they should be able to first grab a list of all bookings for that said apartment.

Grabbing all bookings per apartment requires an `apartmentId`

Here’s the endpoint

```graphql
getAllBookingsPerApartment(apartmentId: String!): [Booking!]!
    @aws_cognito_user_pools
```

The result of this endpoint is a list of `Booking` which also contains a `user` object, depicting the user who made the booking.

```json
"getAllBookingsPerApartment": [
      {
        "apartmentId": "2FGKLMWeMiCJeMZH9OqxEFR0sgh",
        "bookingStatus": "PENDING",
        "endDate": "2022-10-22",
        "id": "2FGKty2bIUaLr0C4Hc513rkX5oT",
        "startDate": "2022-09-22",
        "userId": "treyrosius@gmail.com",
        "user": {
          "email": "treyrosius@gmail.com",
          "firstName": "Rosius",
          "id": "2FGJzw5eiS5pWDUwH9r1PkjROYV",
          "lastName": "Ndimofor Ateh",
          "userType": "ADMIN",
          "verified": true
        }
      },
      {
        "apartmentId": "2FGKLMWeMiCJeMZH9OqxEFR0sgh",
        "bookingStatus": "PENDING",
        "endDate": "2022-10-22",
        "id": "2FGVn4SwbXF8LUsID3tY9lWTziO",
        "startDate": "2022-09-22",
        "userId": "test@gmail.com",
        "user": {
          "email": "test@gmail.com",
          "firstName": "Steve",
          "id": "2FGK3F4WKV28Y9edwsgUjn9gIuG",
          "lastName": "Rosius",
          "userType": "ADMIN",
          "verified": true
        }
      },
      {
        "apartmentId": "2FGKLMWeMiCJeMZH9OqxEFR0sgh",
        "bookingStatus": "PENDING",
        "endDate": "2022-10-22",
        "id": "2FGVr0WV3cqyIJSqOQc7kN4HwFg",
        "startDate": "2022-09-22",
        "userId": "tony@gmail.com",
        "user": {
          "email": "tony@gmail.com",
          "firstName": "Stark",
          "id": "2FGK8BOvlQMDWcQarYtTR2RAQ7a",
          "lastName": "Tony",
          "userType": "TENANT",
          "verified": true
        }
      }
    ]
```

A Single booking object looks like this

```json
 {
        "apartmentId": "2FGKLMWeMiCJeMZH9OqxEFR0sgh",
        "bookingStatus": "PENDING",
        "endDate": "2022-10-22",
        "id": "2FGKty2bIUaLr0C4Hc513rkX5oT",
        "startDate": "2022-09-22",
        "userId": "treyrosius@gmail.com",
        "user": {
          "email": "treyrosius@gmail.com",
          "firstName": "Rosius",
          "id": "2FGJzw5eiS5pWDUwH9r1PkjROYV",
          "lastName": "Ndimofor Ateh",
          "userType": "ADMIN",
          "verified": true
        }
      }
```

Taking a look at the above object, 2 calls where made.

- Get booking
- Get user per booking

We’ll use a Pipeline Resolver coupled with VTL  to easily accomplish this task.

Don’t know about pipeline resolvers yet ? Checkout this well elaborated blog post on how it works.

[Pipeline resolver with cdk,typscript and graphql]([https://phatrabbitapps.com/pipeline-resolvers-with-cdk-v2-typescript-and-graphql](https://phatrabbitapps.com/pipeline-resolvers-with-cdk-v2-typescript-and-graphql))

Inside the file `booking-lambda-stack.ts`, we have to create 2 functions and a resolver.

Function 1 would have request and response mapping templates to `get_all_bookings_apartment`.

Function 2 would have request and response mapping templates to `get_user_per_booking`.

The Resolver would combine both functions and return the results.

Let’s see how that happens in Code.

Inside `lib` folder, create a folder called `vtl` which would contain all our vtl templates . Inside the `vtl` folder, create a file called `before_mapping_template.vtl.`

This file gets the inputs to our endpoint and prepares it to be passed on to the first function. 

In this case, we’ve got just one input which is `apartmentId`.

Type the following code into the created vtl file.

```
#set($result = { "apartmentId": $ctx.args.apartmentId })
$util.toJson($result)
```

Next, create a file called `get_all_bookings_per_apartment_request.vtl` and type in the following code

```

#set($pk = $util.dynamodb.toStringJson("APARTMENT#${ctx.prev.result.apartmentId}"))
 #set($sk =$util.dynamodb.toStringJson("BOOKING#"))
{
    "version" : "2018-05-29",

    "operation" : "Query",
    "limit": $util.toJson($limit),
    "nextToken": $util.toJson($ctx.args.nextToken),
    "query" : {
        "expression": "#PK = :pk and begins_with(#SK,:sk)",
        "expressionNames":{
        "#PK":"PK",
        "#SK":"SK"
        },
        
        "expressionValues" : {
            ":pk" : $pk,
            ":sk" :$sk
        }
    },
    "scanIndexForward" : true

}
```

Notice how we get the `apartmentId` we sent from the previous template. `ctx.prev.result.apartmentId`

Also notice how we’ve used the `begins_with` query function to get all bookings per apartment.

Create a file called `get_all_bookings_per_apartment_responds.vtl` and type in the following code.

```
#if($ctx.error)
    $util.error($ctx.error.message, $ctx.error.type)
#end

$util.toJson($ctx.result)
```

When we get all bookings, each booking object contains a userId. We want to use each `userId` to get the `user` who made the booking for each booking.

In this scenario, we have to use a `GetBatchItem` query, to get all `user` objects at once, instead of individually. It can be used in order to retrieve up to **100 DynamoDB items** in one single DynamoDB request.

This would help limit the number of requests the api makes to dynamoDB and hence speed up our application.

Inside the `vtl` folder, create a file called `get_user_per_booking_request.vtl` and type in the following code.

```
#if($ctx.prev.result.items.size() == 0)
    #return([{}])
#end
#set($keys=[])
#foreach($item in $ctx.prev.result.items)
  $util.qr($keys.add({
    "PK": $util.dynamodb.toDynamoDB("USER#${item.userId}"),
    "SK": $util.dynamodb.toDynamoDB("USER#${item.userId}")
  }))
#end
{
    "version": "2018-05-29",
    "operation": "BatchGetItem",
    "tables" : {
        "AcmsDynamoDBTable": {
            "keys": $util.toJson($keys),
            "consistentRead": true
        }
    }
}
```

From the code above, firstly, we want to do a quick return if there are no available bookings for the apartment. 

If not, then we want to extract the `userId's` of all bookings and create a set of keys to retrieve a list of `user` objects at once using `BatchGetItem`.

Create another file called `get_user_per_booking_responds.vtl` and type in the following code.

```
#set($items= [])
#foreach($item in $ctx.result.data.get("AcmsDynamoDBTable"))
    #set($user=$ctx.prev.result.items.get($foreach.index))
    $util.qr($user.put("user",$item))
    $util.qr($items.add($user))
#end
$util.toJson($items)
```

After retrieving a list of `user` objects, we want to re-assign each user object to their individual bookings.

Create a file called `after_mapping_template.vtl`  and type in the following code.

```
$util.toJson($ctx.result)

```

This file returns the result of the entire process to the resolver.

Now, we have to open up the booking stack and defined 2 functions and a resolver for get all bookings per apartment.

```tsx
const getAllBookingsByApartmentFunction: CfnFunctionConfiguration =
      new CfnFunctionConfiguration(this, "getAllBookingsFunction", {
        apiId: acmsGraphqlApi.attrApiId,

        dataSourceName: acmsTableDatasource.name,
        requestMappingTemplate: readFileSync(
          "./lib/vtl_templates/get_all_bookings_per_apartment_request.vtl"
        ).toString(),
        responseMappingTemplate: readFileSync(
          "./lib/vtl_templates/get_all_bookings_per_apartment_response.vtl"
        ).toString(),
        functionVersion: "2018-05-29",
        name: "getAllBookingsFunction",
      });

    const getUserPerBookingsFunction: CfnFunctionConfiguration =
      new CfnFunctionConfiguration(this, "getUserPerBookingFunction", {
        apiId: acmsGraphqlApi.attrApiId,

        dataSourceName: acmsTableDatasource.name,
        requestMappingTemplate: readFileSync(
          "./lib/vtl_templates/get_user_per_booking_request.vtl"
        ).toString(),
        responseMappingTemplate: readFileSync(
          "./lib/vtl_templates/get_user_per_booking_response.vtl"
        ).toString(),
        functionVersion: "2018-05-29",
        name: "getUserPerBookingFunction",
      });

    const getResultBookingPerApartmentResolver: CfnResolver = new CfnResolver(
      this,
      "getResultBookingPerApartmentResolver",
      {
        apiId: acmsGraphqlApi.attrApiId,
        typeName: "Query",
        fieldName: "getAllBookingsPerApartment",
        kind: "PIPELINE",
        pipelineConfig: {
          functions: [
            getAllBookingsByApartmentFunction.attrFunctionId,
            getUserPerBookingsFunction.attrFunctionId,
          ],
        },

        requestMappingTemplate: readFileSync(
          "./lib/vtl_templates/before_mapping_template.vtl"
        ).toString(),

        responseMappingTemplate: readFileSync(
          "./lib/vtl_templates/after_mapping_template.vtl"
        ).toString(),
      }
    );
```

For the resolver, notice the `kind:PIPELINE` and `pipelineConfig`

Don’t forget to grab the complete code here [https://github.com/trey-rosius/apartment_complex_management_system/blob/master/lib/booking-lambda-stack.ts](https://github.com/trey-rosius/apartment_complex_management_system/blob/master/lib/booking-lambda-stack.ts)

### Lesson 6: User lambda resources

## Lambda Resolver

Inside the `lib` folder, create another folder called `lambda-fns`. 

This folder would contain code for all our lambda functions and entities.
Let’s create files and folders specific to the user endpoints and entities.

Inside the `lambda-fns` folder, create another folder called `user`.

Create 3 typescript files inside the `user` folder.

- main.ts
- userEntity.ts
- createUserAccounts.ts

`main.ts` would serve as our ,lambda handler, routing all user endpoints to their respective destinations.

Inside the user stack, defined your lambda resource as follows

```tsx
const codeSigningConfig = new lambda.CodeSigningConfig(
      this,
      "CodeSigningConfig",
      {
        signingProfiles: [signingProfile],
      }
    );
    const acmsLambda = new NodejsFunction(this, "AcmsUserHandler", {
      tracing: Tracing.ACTIVE,
      codeSigningConfig,
      runtime: lambda.Runtime.NODEJS_16_X,
      handler: "handler",
      entry: path.join(__dirname, "lambda-fns/user", "main.ts"),

      memorySize: 1024,
    });

```

The first endpoint we are going to implement is the `createUserAccount` endpoint, which takes input 

```graphql
input UserInput {
  firstName: String!
  lastName: String!
  email: String!
  verified: Boolean!
  userType: UserType!
}
```

Also define the lambda datasource and resolver resources as follows inside the user stack.

```tsx
const lambdaDataSources: CfnDataSource = new CfnDataSource(
      this,
      "ACMSLambdaDatasource",
      {
        apiId: acmsGraphqlApi.attrApiId,
        name: "ACMSLambdaDatasource",
        type: "AWS_LAMBDA",

        lambdaConfig: {
          lambdaFunctionArn: acmsLambda.functionArn,
        },
        serviceRoleArn: appsyncLambdaRole.roleArn,
      }
    );

    const createUserAccountResolver: CfnResolver = new CfnResolver(
      this,
      "createUserAccountResolver",
      {
        apiId: acmsGraphqlApi.attrApiId,
        typeName: "Mutation",
        fieldName: "createUserAccount",
        dataSourceName: lambdaDataSources.attrName,
      }
    );
```

Grant permissions and add `dependsOn`.

```tsx
    createUserAccountResolver.addDependsOn(apiSchema);
    acmsDatabase.grantFullAccess(acmsLambda);
    acmsLambda.addEnvironment("ACMS_DB", acmsDatabase.tableName);
```

Grab the complete code here [https://github.com/trey-rosius/apartment_complex_management_system/blob/master/lib/user-lambda-stack.ts](https://github.com/trey-rosius/apartment_complex_management_system/blob/master/lib/user-lambda-stack.ts)

Inside the `main.ts` file, type in the following code

```tsx
import { Logger } from "@aws-lambda-powertools/logger";
import createUserAccount from "./createUserAccounts";
import { AppSyncResolverEvent, Context } from "aws-lambda";

const logger = new Logger({ serviceName: "ApartmentComplexManagementApp" });

type UserInput = {
  firstName: string;
  lastName: string;
  email: string;
  verified: boolean;
  userType: string;
};

exports.handler = async (
  event: AppSyncResolverEvent<UserInput>,
  context: Context
) => {
  logger.addContext(context);
  logger.info(
    `appsync event arguments ${event.arguments} and event info ${event.info}`
  );
  switch (event.info.fieldName) {
    case "createUserAccount":
      return await createUserAccount(event.arguments, logger);

    default:
      return null;
  }
};
```

Inside the `createUserAccount` file, type in the following code. This file takes 2 arguments.

- UserInput
- Logger

```tsx
import { Logger } from "@aws-lambda-powertools/logger";
import UserEntity from "./userEntity";
import { DynamoDB } from "aws-sdk";
import { uuid } from "../../utils";

type UserInput = {
  firstName: string;
  lastName: string;
  email: string;
  verified: boolean;
  userType: string;
};
type UserReturnParameters = {
  id: string;
  ENTITY: string;
  firstName: string;
  lastName: string;
  verified: boolean;
  email: string;
  userType: string;
  updatedOn: string;
  createdOn: string;
};

async function createUserAccount(
  input: UserInput,
  logger: Logger
): Promise<UserReturnParameters> {
  const documentClient = new DynamoDB.DocumentClient();
//DynamoDB table name
  let tableName = process.env.ACMS_DB;
  const createdOn = Date.now().toString();
  const id: string = uuid();
  if (tableName === undefined) {
    logger.error(`Couldn't get the table name`);
    tableName = "AcmsDynamoDBTable";
  }

//User Entity
  const userInput: UserEntity = new UserEntity({
    id: id,
    ...input,
    createdOn,
  });

  logger.info(`create user input info", ${userInput}`);
  const params = {
    TableName: tableName,
    Item: userInput.toItem(),
    ConditionExpression: "attribute_not_exists(PK)",
  };

  try {
    await documentClient.put(params).promise();
    return userInput.graphQlReturn();
  } catch (error: any) {
    if (error.name === "ConditionalCheckFailedException")
      logger.error(`an error occured while creating user ${error}`);
    throw Error("A user with same email address already Exist");
  }
}
export default createUserAccount;
```

Firstly, we defined structures for the `UserInput` and `UserReturnParameters`. Then we instantiate DynamoDb Document client, populate a `UserEntity` class and carryout a DynamoDB `put` transaction. 

Also, we want to make sure that a user with that particular email doesn’t already exist in the database. So we use `attribute_not_exists(PK)`.

Here’s how the `userEntity` class looks like 

```tsx
interface UserParameters {
  id: string;
  firstName: string;
  lastName: string;
  verified: boolean;
  email: string;
  userType: string;
  createdOn: string;
  updatedOn?: string;
}
class UserEntity {
  id: string;
  firstName: string;
  lastName: string;
  verified: boolean;
  email: string;
  userType: string;
  createdOn: string;
  updatedOn: string;

  constructor({
    id,
    firstName,
    lastName,
    verified,
    email,
    userType,
    createdOn,
    updatedOn,
  }: UserParameters) {
    this.id = id;
    this.firstName = firstName;
    this.lastName = lastName;
    this.verified = verified;
    this.email = email;
    this.userType = userType;
    this.updatedOn = updatedOn ?? "";

    this.createdOn = createdOn;
  }

  key(): {
    PK: string;
    SK: string;
  } {
    return {
      PK: `USER#${this.email}`,
      SK: `USER#${this.email}`,
    };
  }

  toItem() {
    return {
      ...this.key(),
      id: this.id,
      ENTITY: "USER",
      firstName: this.firstName,
      lastName: this.lastName,
      verified: this.verified,
      email: this.email,
      userType: this.userType,
      updatedOn: this.updatedOn,
      createdOn: this.createdOn,
    };
  }

  graphQlReturn() {
    return {
      id: this.id,
      ENTITY: "USER",
      firstName: this.firstName,
      lastName: this.lastName,
      verified: this.verified,
      email: this.email,
      userType: this.userType,
      updatedOn: this.updatedOn,
      createdOn: this.createdOn,
    };
  }
}

export default UserEntity;
```

The last step is to add the user stack to the app. 

Navigate to the `bin` folder and open up the app file. Mine is `acms.ts`.

Modify the file contents to look like this now.

```tsx
const app = new cdk.App();
const acmsStack = new AcmsStack(app, "AcmsStack", {
  env: { account: "13xxxxxxxxxx", region: "us-east-2" },

  /* For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html */
});

new UserLamdaStacks(app, "UserLambdaStacks", {
  env: { account: "13xxxxxxxxxx", region: "us-east-2" },
  acmsDatabase: acmsStack.acmsDatabase,
  apiSchema: acmsStack.apiSchema,
  acmsGraphqlApi: acmsStack.acmsGraphqlApi,
});
```

### Deploy

You can grab the complete code for the `acms` and `userStacks` and deploy using 

```tsx
cdk bootstrap
cdk deploy --all
```

### Lesson 7: Acms stack

### ACMS Stack

In this stack construct, we are going to provision the following infrastructure resources

- Cognito UserPool
- AppSync GraphQL Api
- DynamoDb Table
- CloudWatch and DynamoDB role managed Policies.

Inside `acms-stack.ts` file located in `lib` folder, we’ll define constructs for the above resources.

And because we’ll be using the resources in other stacks, we have to expose the resources somehow. 

We’ll see that in a bit.

### Cognito UserPool

Let’s define the userpool and the userpool client

```jsx
/**
 * UserPool and UserPool Client
 */
const userPool: UserPool = new cognito.UserPool(this, "ACMSCognitoUserPool", {
  selfSignUpEnabled: true,
  accountRecovery: cognito.AccountRecovery.PHONE_AND_EMAIL,
  userVerification: {
    emailStyle: cognito.VerificationEmailStyle.CODE,
  },
  autoVerify: {
    email: true,
  },
  standardAttributes: {
    email: {
      required: true,
      mutable: true,
    },
  },
});

const userPoolClient: UserPoolClient = new cognito.UserPoolClient(
  this,
  "ACMSUserPoolClient",
  {
    userPool,
  }
);
```

### Lesson 8: Apartment stack

### Apartments Stack.

The apartment stack follows the same concept  and code structure as the user and building stacks. 

So we’ll dive straight to testing.

You can grab the complete code here.

[Complete Code](https://github.com/trey-rosius/apartment_complex_management_system/blob/master/lib/apartment-lambda-stack.ts)

### Testing Apartment Stack

```graphql
createApartment(input: ApartmentInput): Apartment!
    @aws_cognito_user_pools(cognito_groups: ["Admins"])
```

This endpoint is only accessible to users belonging the the group `Admins` .

Since we already have a user belonging to this group, we’ll just go ahead and run the endpoint.

![alt text](https://d14x58xoxfhz1s.cloudfront.net/61a3dbcb-edea-4c91-bcb7-325b9356fd85)

You can also run the endpoint multiple times with different inputs, to create multiple apartments for that building.

### Lesson 9: Process sqs booking

### `processSqsBooking.ts`

In this function, we poll the messages from the SQS queue and save them to dynamoDB

```tsx
const promises = event.Records.map(async (value: SQSRecord) => {
    try {
      const bookingDetails: PutItemInputAttributeMap = JSON.parse(value.body);
      if (tableName === undefined) {
        logger.error(`Couldn't get the table name`);
        tableName = "AcmsDynamoDBTable";
      }
      const params = {
        TableName: tableName,
        Item: bookingDetails,
      };

      logger.info(`put parameters for booking is ${JSON.stringify(params)}`);
      await documentClient.put(params).promise();
    } catch (error) {
      logger.error(
        `an error occured during put booking ${JSON.stringify(error)}`
      );
      failedMessageIds.push(value.messageId);
    }
  });
  // execute all promises
  await Promise.all(promises);

  return {
    batchItemFailures: failedMessageIds.map((id) => {
      return {
        itemIdentifier: id,
      };
    }),
  };
```

Grab the complete code on [Github](https://github.com/trey-rosius/apartment_complex_management_system).

Deploy your CDK application and test.

### Lesson 10: Graphql api and schema

### GraphQL API and Schema.

In the root directory of your project, create a folder called `schema`. Inside this folder, create a file called `schema.graphql`.

Type this into the `schema.graphql` file.

```graphql
schema {
  query: Query
  mutation: Mutation
  subscription: Subscription
}

type Mutation {
  createUserAccount(input: UserInput!): User! @aws_cognito_user_pools
  updateUserAccount(input: UpdateUserInput!): User! @aws_cognito_user_pools
  deleteUserAccount(id: ID!): Boolean! @aws_cognito_user_pools

  createBuilding(input: BuildingInput!): Building!
    @aws_cognito_user_pools(cognito_groups: ["Admins"])

  createApartment(input: ApartmentInput): Apartment!
    @aws_cognito_user_pools(cognito_groups: ["Admins"])

  createApartmentBooking(input: CreateBookingInput!): Booking!
    @aws_cognito_user_pools(cognito_groups: ["Tenants"])
}

type Subscription {
  onCreateApartmentBooking: Booking
    @aws_cognito_user_pools
    @aws_subscribe(mutations: ["createApartmentBooking"])
}

type Query {
  getUserAccount(id: ID!): User! @aws_cognito_user_pools
  getBookings(bookingId: String): Booking

  getAllUserAccounts(pagination: Pagination): UsersResult!
    @aws_cognito_user_pools(cognito_groups: ["Admins", "Caretakers"])

  getAllBookingsPerApartment(apartmentId: String!): [Booking!]!
    @aws_cognito_user_pools(cognito_groups: ["Admins", "Caretakers"])
}

input CreateBookingInput {
  userId: String!
  apartmentId: String!
  startDate: AWSDate!
  endDate: AWSDate!
  bookingStatus: BookingStatus!
}

input BuildingInput {
  name: String!
  userId: String!
  numberOfApartments: Int!
  address: AddressInput!
}

type Address @aws_cognito_user_pools {
  streetAddress: String!
  postalCode: String!
  city: String!
  country: String!
}
input AddressInput {
  streetAddress: String!
  postalCode: String!
  city: String!
  country: String!
}
type User @aws_cognito_user_pools {
  id: ID!
  firstName: String!
  lastName: String!
  email: String!
  verified: Boolean!
  userType: UserType!
  updatedOn: AWSDateTime
  createdOn: AWSDateTime!
}
type Booking @aws_cognito_user_pools {
  id: ID!
  userId: String!
  user: User!
  startDate: AWSDate!
  endDate: AWSDate!
  apartmentId: String!
  bookingStatus: BookingStatus!
  updateOn: AWSDateTime!
  createdOn: AWSDateTime!
}

enum BookingStatus {
  PENDING
  APPROVED
  CANCELLED
}

input UserInput {
  firstName: String!
  lastName: String!
  email: String!
  verified: Boolean!
  userType: UserType!
}

input UpdateUserInput {
  firstName: String!
  lastName: String!
  verified: Boolean!
  userType: UserType!
}

type Building @aws_cognito_user_pools {
  id: ID!
  userId: String!
  name: String!
  address: Address!
  numberOfApartments: Int!
  apartments: [Apartment!]
  updateOn: AWSDateTime!
  createdOn: AWSDateTime!
}

type Apartment @aws_cognito_user_pools {
  id: ID!
  apartmentNumber: String!
  building: Building!
  tenant: User!
  caretaker: User!
  apartmentType: ApartmentType!
  apartmentStatus: ApartmentStatus!
  kitchen: Boolean!
  numberOfRooms: Int!
  createdOn: AWSDateTime!
}

input ApartmentInput @aws_cognito_user_pools {
  apartmentNumber: String!
  buildingId: String!
  numberOfRooms: Int!
  apartmentType: ApartmentType!
  apartmentStatus: ApartmentStatus!
}
type UsersResult @aws_cognito_user_pools {
  items: [User!]!
  nextToken: String
}

input Pagination {
  limit: Int
  nextToken: String
}

enum ApartmentType {
  SINGLE_ROOM
  DOUBLE_ROOM
  VILLA
}
enum ApartmentStatus {
  VACANT
  OCCUPIED
}
enum UserType {
  ADMIN
  TENANT
  CARETAKER
}
```

In the schema file above, we have different access levels for mutations and queries. For example,

- Only `Admin` can create a building or an apartment.
- Both `Admins` and `Caretakers` can `getAllBookingsPerApartment`. And a lot more.

Let’s go ahead to define

- GraphQL API
- GraphQL Schema
- GraphQL Datasource

Since we’ll be needing the graphql api and datasource construct definitions in other stacks, we need to expose them.

Here’s how it’s done. Firstly, initialize your construct like so

```jsx
export class AcmsStack extends Stack {
  public readonly acmsGraphqlApi: CfnGraphQLApi;
  public readonly apiSchema: CfnGraphQLSchema;
  public readonly acmsTableDatasource: CfnDataSource;
```

Then, define them like so

```jsx
/**
 * GraphQL API
 */
this.acmsGraphqlApi = new CfnGraphQLApi(this, "acmsGraphqlApi", {
  name: "ACMS",
  authenticationType: "API_KEY",

  additionalAuthenticationProviders: [
    {
      authenticationType: "AMAZON_COGNITO_USER_POOLS",

      userPoolConfig: {
        userPoolId: userPool.userPoolId,
        awsRegion: "us-east-2",
      },
    },
  ],
  userPoolConfig: {
    userPoolId: userPool.userPoolId,
    defaultAction: "ALLOW",
    awsRegion: "us-east-2",
  },

  logConfig: {
    fieldLogLevel: "ALL",
    cloudWatchLogsRoleArn: cloudWatchRole.roleArn,
  },
  xrayEnabled: true,
});

/**
 * Graphql Schema
 */

this.apiSchema = new CfnGraphQLSchema(this, "ACMSGraphqlApiSchema", {
  apiId: this.acmsGraphqlApi.attrApiId,
  definition: readFileSync("./schema/schema.graphql").toString(),
});

this.acmsTableDatasource = new CfnDataSource(
  this,
  "AcmsDynamoDBTableDataSource",
  {
    apiId: this.acmsGraphqlApi.attrApiId,
    name: "AcmsDynamoDBTableDataSource",
    type: "AMAZON_DYNAMODB",
    dynamoDbConfig: {
      tableName: this.acmsDatabase.tableName,
      awsRegion: this.region,
    },
    serviceRoleArn: dynamoDBRole.roleArn,
  }
);
```

The default authentication type for the GraphQl api is the `API_KEY`.

With this auth type, users can see a list of all available buildings on the platform. But they’ll need to be signed in and assigned to a particular group, in-order to progress through the rest of the api endpoints.

## Outputs

```jsx
new CfnOutput(this, "UserPoolId", {
  value: userPool.userPoolId,
});
new CfnOutput(this, "UserPoolClientId", {
  value: userPoolClient.userPoolClientId,
});

new CfnOutput(this, "GraphQLAPI ID", {
  value: this.acmsGraphqlApi.attrApiId,
});

new CfnOutput(this, "GraphQLAPI URL", {
  value: this.acmsGraphqlApi.attrGraphQlUrl,
});
```

You can view the complete code [here](https://github.com/trey-rosius/apartment_complex_management_system/blob/master/lib/acms-stack.ts)

