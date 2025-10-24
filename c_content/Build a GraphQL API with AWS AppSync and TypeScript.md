# Build a GraphQL API with AWS AppSync and TypeScript

## Overview



# Build a GraphQL API with AWS AppSync and TypeScript

Welcome! In this workshop, you will learn how to build a fully functional GraphQL API from scratch utilizing serverless technology such as AWS AppSync, Amazon DynamoDB and Amazon Cognito. 

We will cover aspects like authentication, authorization and real-time pub/sub. 

To accomplish this, we will use TypeScript as our main programming language, and the Serverless Framework for Infrastructure as Code (IaC). We will use the direct-integration between AppSync and DynamoDB (zero Lambda function required).

The full workshop should take you about 2 hours to complete.

## About the Instructor


Hi 👋, I'm Benoit, a passionate serverless developer with a deep love for serverless technology. As an AWS Community Builder, I actively contribute to the community and share my expertise. 

You can often hear me promoting AWS AppSync, one of my favourite AWS services. As such, I am the core maintainer of the [serverless-appsync-plugin](https://github.com/sid88in/serverless-appsync-plugin). 

I am also the creator of [appsync.wtf](https://appsync.wtf)) and [GraphBolt](https://graphbolt.dev). 

My journey involves creating engaging content about serverless, aiming to simplify and share knowledge within the tech community. Connect with me on Twitter/X [@Benoit_Boure](https://twitter.com/Benoit_Boure).



## Description
In this workshop, you will learn how to build a fully functional GraphQL API from scratch utilizing serverless technology such as AWS AppSync, Amazon DynamoDB, and Amazon Cognito. We will cover aspects like authentication, authorization, and real-time pub/sub.

## Course Details
- **Number of Modules:** 4
- **Image:** https://d14x58xoxfhz1s.cloudfront.net/73495160-623c-4c9a-b56e-788773d24682
- **Difficulty:** Intermediate
- **Framework:** Serverless,Serverless framework
- **Programming_language:** Typescript
- **Web_framework:** 
- **Mobile_framework:** 
- **ServerlessTopic:** serverless_architecture
- **MainCourse:** true
- **MainCourseId:** N/A
- **Trailer:** 
- **Video:** N/A
- **File:** N/A
- **CodeVisible:** false
- **UploadVisible:** false
- **Tasks:** false
- **Publish:** true
- **ProposedCourses:** 
- **AuthorId:** 37b03192-d1dc-4c71-b2ae-8725e2eb735d
- **AuthorGroup:** student
- **Duration:** 6 hours
- **Featured:** N/A
- **DefaultMedia:** N/A
- **NumberOfLessons:** 15
- **CreatedAt:** 2024-06-13T00:55:20.251Z
- **UpdatedAt:** 2024-11-26T10:02:43.866Z
- **CourseCategoryCourseId:** ac49bd8c-68fe-45c4-8b6a-37bf9ee28389
- **_version:** 22
- **_lastChangedAt:** 1732615363913
- **_deleted:** N/A

## Module 1: Get started

### Lesson 1: Clone the Repository


## Clone the Project

First, we will clone the project and get familiar with it. Run the following command and open it in your favorite IDE.

```bash
git clone git@github.com:bboure/appsync-typescript-workshop.git
```

## Workspace Structure

The working directory should look like this.

```bash
├── codegen.ts
├── definitions
│   ├── appsync.ts
│   ├── cognito.ts
│   └── dynamodb.ts
├── schema
│   └── schema.graphql
├── serverless.ts
└── src
    ├── resolvers
    │   └── Query.getTask.ts
    ├── types
    │   ├── db.ts
    │   └── schema.ts
    └── utils.ts
```

- `codegen.ts` contains GraphQL codegen configuration (More on that below).
- `definitions` is a directory containing files with Serverless Framework definitions.
- `schema` is a directory containing the schema for our API.
- `serverless.ts` is the entry point of our Serverless Framework definitions.
- `src` will contain the business logic for our API as well as some TypeScript types.


### Lesson 2: The Graphql Schema



## The GraphQL Schema

Open `schema/schema.graphql`. It contains a basic schema for our API, including several types (e.g. `Task` and `Project`), some queries (e.g. `getTask`), and mutations (`createTask`).

To learn more about types, fields, and GraphQL schemas, go to the [GraphQL docs](https://graphql.org/learn/schema/#object-types-and-fields).

## TypeScript

AWS AppSync allows us to write resolvers in JavaScript. This means that to have better auto-complete capabilities and safeguard us from making mistakes, we can also use TypeScript.

By default, AWS AppSync does not support TypeScript. Instead, it supports a [limited flavor of JavaScript](https://blog.graphbolt.dev/everything-you-should-know-about-the-appsync-javascript-pipeline-resolvers). Luckily, the serverless-appsync-plugin automatically [transpiles and bundles TypeScript into AppSync-compatible Javascript](https://github.com/sid88in/serverless-appsync-plugin/blob/master/doc/general-config.md#Esbuild) code, out of the box.

## Eslint

In our project, we installed and configured eslint (`.eslintrc.json`). This gives us linting capabilities about good practices when writing code in TypeScript. However, AppSync does not support all of the “standard” JavaScript/TypeScript features.

The AppSync team provides a useful eslint plugin that warns us about invalid usage: [@aws-appsync/eslint-plugin](https://www.npmjs.com/package/@aws-appsync/eslint-plugin)

We are using the plugin in this project, but because we only want it to be active inside the resolvers code, we use an additional eslint config file that we placed in the `src/resolvers` directory. 

This way, those special rules only apply to resolvers, and not the rest of our codebase (for example, Lambda functions).

```json
{
  "extends": ["plugin:@aws-appsync/base"]
}
```

## Codegen

[GraphQL Codegen](https://the-guild.dev/graphql/codegen) is an open-source library that provides tools to generate code from GraphQL schemas. In this project, we will use it to generate the TypeScript types of our API. It uses the definition in `codegen.ts`.

Run the following command.

```bash
npm run codegen
```

Now have a look at `src/types/schema.ts`. You should see a set of TypeScript types that match our schema. We will use them later to build our API.

## Module 2: Build

### Lesson 1: Define the Resolvers

# Resolvers

Data sources define how our API can access the data stores, but we still need to define how the data connects to the GraphQL schema. For that, GraphQL (and AWS AppSync) use resolvers. 

Resolvers are like functions that are executed in order to generate the data source request on one hand, and handle their responses on the other hand.

![DataSources And Resolvers](https://d14x58xoxfhz1s.cloudfront.net/5ee212b6-6e78-4f83-9bfa-919ab23413ad)


Open the `definitions/appsync.ts` file and add the following code inside `resolvers`.

```tsx showLineNumbers
// Tasks
'Query.getTask': {
  dataSource: 'tasks',
  kind: 'UNIT',
  code: 'src/resolvers/Query.getTask.ts',
},
'Query.listTasks': {
  dataSource: 'tasks',
  kind: 'UNIT',
  code: 'src/resolvers/Query.listTasks.ts',
},
'Mutation.createTask': {
  dataSource: 'tasks',
  kind: 'UNIT',
  code: 'src/resolvers/Mutation.createTask.ts',
},
'Mutation.updateTask': {
  dataSource: 'tasks',
  kind: 'UNIT',
  code: 'src/resolvers/Mutation.updateTask.ts',
},
'Mutation.deleteTask': {
  dataSource: 'tasks',
  kind: 'UNIT',
  code: 'src/resolvers/Mutation.deleteTask.ts',
},
'Task.project': {
  dataSource: 'projects',
  kind: 'UNIT',
  code: 'src/resolvers/Task.project.ts',
},
// Projects
'Query.getProject': {
  dataSource: 'projects',
  kind: 'UNIT',
  code: 'src/resolvers/Query.getProject.ts',
},
'Mutation.createProject': {
  dataSource: 'projects',
  kind: 'UNIT',
  code: 'src/resolvers/Mutation.createProject.ts',
},
'Mutation.updateProject': {
  dataSource: 'projects',
  kind: 'UNIT',
  code: 'src/resolvers/Mutation.updateProject.ts',
},
'Mutation.deleteProject': {
  dataSource: 'projects',
  kind: 'UNIT',
  code: 'src/resolvers/Mutation.deleteProject.ts',
},
'Mutation.addUserToProject': {
  dataSource: 'projectUsers',
  kind: 'UNIT',
  code: 'src/resolvers/Mutation.addUserToProject.ts',
},
```

`resolvers` is a key-value pair object that represents resolver definitions.

The key specifies the GraphQL type and field that the resolver is attached to. For example, for `Query.getTask` , it means that the resolver is attached to the `getTask` field of the `Query` type. 

`Query` and `Mutation` are two special types in GraphQL that correspond to queries and mutations, respectively.

Note that you can attach a resolver to a field of custom types too. For example, `Task.project` (lines 27-31) defines the resolver for a tasks' project.

The value represents the definition of the resolver.

- `dataSource` is a reference to the data source name where the data lives. This is the data source that the resolver will invoke after generating the request.
- `kind`: There are two kinds of resolvers: `UNIT` and `PIPELINE`. We will learn about pipeline resolvers later in this workshop. For now, we will use the simpler `UNIT` kind.
- `code` is the path to the resolver code. Resolvers are written in TypeScript. We will get to know them better in a minute.

For more details about resolver definitions, check the [documentation](https://github.com/sid88in/serverless-appsync-plugin/blob/master/doc/resolvers.md).

## Deploy

We can now deploy our API again to make the latest changes effective.

```shell
npx sls deploy
```

While the changes are being deployed, let's have a look at the resolvers code and understand them.

##  Resolvers

To make things smoother for you, I have already written all the necessary resolvers. Let's have a look and understand how they work.

For example, let's take `getTask` (`src/resolvers/Query.getTask.ts`)

```tsx showLineNumbers
import { Context, util } from '@aws-appsync/utils';
import { get } from '@aws-appsync/utils/dynamodb';
import { QueryGetTaskArgs } from '../types/schema';
import { DBTask } from '../types/db';

export const request = (ctx: Context<QueryGetTaskArgs>) => {
  return get<DBTask>({
    key: {
      id: ctx.args.id,
    },
  });
};

export const response = (ctx: Context<QueryGetTaskArgs>) => {
  if (!ctx.result) {
    util.error('Task not found', 'NotFound');
  }

  return ctx.result;
};
```

Resolvers are composed of two functions, also known as _handlers._

The _request_ handler is used to generate the request to the data source. In this case, it's a DynamoDB request and we want to execute a `GetItem` operation.

The `@aws-appsync/utils/dynamodb` package comes with a bunch of useful functions to help us generate DynamoDB requests. Here, we are using `get` and we are passing it the `key` of the item we want to retrieve. 

It contains the name of the key attribute (`id`) and its value which is coming from the GraphQL query as an argument. `ctx.args` is an object that corresponds to the GraphQL arguments as defined in the schema.

```graphql
type Query {
  getTask(id: ID!): Task!
}
```

For more information about all the DynamoDB helpers, check the [documentation](https://docs.aws.amazon.com/appsync/latest/devguide/built-in-modules-js.html#built-in-ddb-modules).

The _response_ handler receives the data from the data source. This is where you can transform it and map it to the GraphQL schema. Here we just return the data received from DynamoDB in `crx.result`. Before that, we check that the item exists, and if it does not we return an error with `util.error()`.

Both the _request_ and _response_ handlers receive an object as first argument (called the context). The `context` object contains information about the incoming request (input arguments, identity, etc.) as well as the interaction with the data source (e.g. the result, errors that might have ocurred, etc) (only in _response_). You can learn more about it in the [documentation](https://docs.aws.amazon.com/appsync/latest/devguide/resolver-context-reference-js.html).

## TypeScript in Resolvers

As we commented earlier in this workshop, we wrote resolvers in TypeScript. We also learned about GraphQL codegen, and we generated TypeScript types from our GraphQL schema. Keen eyes might have spotted that we used those types in our resolvers. For example:

```tsx
export const request = (ctx: Context<QueryGetTaskArgs>) => {
  // ...
};
```

`QueryGetTaskArgs` is an auto-generated type that represents the input arguments of the `getTask` Query.

You might also have noticed the `DBTask` type in the same resolver. This is a custom type that I created and represents the DynamoDb `Task` entity. 

This is because data source entities and GraphQL types don't always have a one to one correspondence. For example, the `Task` type in GraphQL has a `project` field which represents the Project the task belongs to. 

Project has its own entity and data store, so it is excluded from the `DBTask` type. Similarly, `DBTask` has a `projectId` which is not present in the GraphQL schema.

If you look in the schema (`schema/schema.graphql`), you will notice that I used `interface`s. For example, `ITask`.

```graphql
interface ITask {
  id: ID!
  title: String!
  description: String!
  priority: Int!
  status: Status!
  assignees: [ID!]!
  createdAt: AWSDateTime!
  updatedAt: AWSDateTime!
}
```

The interface defines basic scalar types only that both the schema and the database have. Later, I use this interface in the definition of the `Task` type where I define additional complex fields (e.g. `project`).

```graphql
type Task implements ITask {
  id: ID!
  title: String!
  description: String!
  priority: Int!
  status: Status!
  project: Project!
  assignees: [ID!]!
  createdAt: AWSDateTime!
  updatedAt: AWSDateTime!
}
```

I did the same when defining the database entity type.

```ts
export type DBTask = ITask & {
  projectId: string;
};
```

I will now let you explore the remaining resolvers. Observe the usage of the dynamodb helpers, how the requests are generated and responses are handled, and how the different TypeScript types are used. When you are done, come back here and continue.

### Lesson 2: Testing


# Testing

## Create a User in Cognito

We should now have a fully working API. Let's test it, but for that we need a user to authenticate with.

To do so, connect to the AWS console, and go to [Amazon Cognito](https://us-east-1.console.aws.amazon.com/cognito/v2/idp/user-pools).

Open the Cognito user pool name `AWS AppSync Workshop User Pool` and go to _App Integrations_. Under _App clients and analytics_, copy the clientId of the `AWS AppSync Workshop Client`.

Then execute this command, replace the following values:

- `clientId` The client id you copied in Amazon Cognito
- `username` Pick a name for your user
- `password` Pick a password. Passwords must contain at least 8 characters, have at least one number, one lowercase character, one uppercase character and one special character.
- `email` the email address of your user. The email must be real and valid. You will need to validate it in the following step.

```bash
aws cognito-idp sign-up --client-id "{clientId}" --username "{username}" --password "{password}" --user-attributes Name=email,Value="{email}"
```

example

```bash
aws cognito-idp sign-up --client-id "3un93evcbfcc87jdp6jfc94ig0" --username "ben" --password "AppSync101!" --user-attributes Name=email,Value="ben@example.com"
```

```json
{
  "UserConfirmed": false,
  "CodeDeliveryDetails": {
    "Destination": "b***@g***",
    "DeliveryMedium": "EMAIL",
    "AttributeName": "email"
  },
  "UserSub": "de42fece-e9c5-4c89-933e-7647ef8aa1f9"
}
```

You should immediately receive an email with a verification code. Copy the code and execute the following command. Again, replace the appropriate values.

```bash
aws cognito-idp confirm-sign-up --client-id "{clientId}" --username "{username}" --confirmation-code {verificationCode}
```

If the command does not return any error, it means it worked as expected.

## Test Queries and Mutations

Now that you have a user, it's time to try a few Queries and Mutations. For that, you can use the GraphQL client of your choice (e.g. Postman), but I invite you to use [GraphBolt](https://graphbolt.dev). 

GraphBolt is a desktop app that helps developers build, test and debug AWS AppSync APIs. It comes with a GraphQL client that is specially tailored for AWS AppSync.

If you prefer, you can also use the [AWS AppSync console](https://us-east-1.console.aws.amazon.com/appsync/home?region=us-east-1#/apis). Open the created API and go to the _Queries_ tab.

Since we are starting from scratch, we don't have any data in our Database. Let's start by creating a Project first.

Login with your username and password. if you are using GraphBolt, you can do so by clicking on the padlock icon on the top right ([see documentation](https://docs.graphbolt.dev/graphql-client/authentication)). 

From the AWS AppSync console, click on **Login with User Pool**. In both cases, you will need to select the user pool, client and enter your username and password.

Execute the following request.

```graphql
mutation CreateProject {
  createProject(input: { name: "Project1", description: "My first Project" }) {
    id
    name
    description
    createdAt
    updatedAt
  }
}
```

If everything went well, you should see a result like this one:

```json
{
  "data": {
    "createProject": {
      "id": "1d49e592-e489-43cc-8ce5-d7d99a731cc4",
      "name": "Project1",
      "description": "My first Project",
      "createdAt": "2024-01-11T17:29:57.809Z",
      "updatedAt": "2024-01-11T17:29:57.809Z"
    }
  }
}
```

Now, go to DynamoDB, and open the `Projects` table. (its name should be `appsync-typescript-workshop-dev-projects`). You should see that the item was persisted.

![DynamoDB Project Item](https://d14x58xoxfhz1s.cloudfront.net/c4f7e85f-ffcf-4c5a-a6f1-0609e235b634)

Do the same, and create a new Task. Don't forget to replace `projectId` with the id of the project that was previously created. Also, replace `ben` with your own username in `assignees`.

```graphql
mutation CreateTask {
  createTask(
    input: {
      title: "Task 1"
      description: "My first task"
      priority: 10
      status: TODO
      projectId: "1d49e592-e489-43cc-8ce5-d7d99a731cc4"
      assignees: ["ben"]
    }
  ) {
    id
    title
    description
    priority
    status
    createdAt
    updatedAt
    assignees
  }
}
```

```json
{
  "data": {
    "createTask": {
      "id": "ef01da5e-79fd-4e56-97f0-e755f7b82d8c",
      "title": "Task 1",
      "description": "My first task",
      "priority": 10,
      "status": "TODO",
      "createdAt": "2024-01-11T17:34:51.546Z",
      "updatedAt": "2024-01-11T17:34:51.546Z",
      "assignees": ["ben"]
    }
  }
}
```

Great. I'll let you play with other requests. Try to create a few more tasks and projects, then use the `Query.listTasks` to get all the tasks from a project. Also try to update and delete tasks using the `updateTask` and `deleteTask` mutations.

### Lesson 3: Define the Datasources

# Defining Data Sources

We now have a deployed API, but it does not do anything yet. In this section we will create our DynamoDB tables and allow our API to interact with them.

![DataSources And Resolvers](https://d14x58xoxfhz1s.cloudfront.net/757881e4-a895-4e3d-b6e5-e1cf3eca4045)

## DynamoDB Tables

As our primary data store, we will use DynamoDB. DynamoDB is a fully managed and serverless key-value store with single-digit latency.

Open the `definitions/dynamodb.ts` file and add the following code under _`// 2.1. Define the DynamoDB tables`_

```tsx showLineNumbers
Tasks: {
  Type: 'AWS::DynamoDB::Table',
  Properties: {
    TableName: '${self:service}-${sls:stage}-tasks',
    BillingMode: 'PAY_PER_REQUEST',
    AttributeDefinitions: [
      {
        AttributeName: 'id',
        AttributeType: 'S',
      },
      {
        AttributeName: 'projectId',
        AttributeType: 'S',
      },
      {
        AttributeName: 'createdAt',
        AttributeType: 'S',
      },
    ],
    KeySchema: [
      {
        AttributeName: 'id',
        KeyType: 'HASH',
      },
    ],
    GlobalSecondaryIndexes: [
      {
        IndexName: 'byProject',
        KeySchema: [
          {
            AttributeName: 'projectId',
            KeyType: 'HASH',
          },
          {
            AttributeName: 'createdAt',
            KeyType: 'RANGE',
          },
        ],
        Projection: {
          ProjectionType: 'ALL',
        },
      },
    ],
  },
},
Projects: {
    Type: 'AWS::DynamoDB::Table',
    Properties: {
      TableName: '${self:service}-${sls:stage}-projects',
      BillingMode: 'PAY_PER_REQUEST',
      AttributeDefinitions: [
        {
          AttributeName: 'id',
          AttributeType: 'S',
        },
      ],
      KeySchema: [
        {
          AttributeName: 'id',
          KeyType: 'HASH',
        },
      ],
    },
},
ProjectUsers: {
  Type: 'AWS::DynamoDB::Table',
  Properties: {
    TableName: '${self:service}-${sls:stage}-project-users',
    BillingMode: 'PAY_PER_REQUEST',
    AttributeDefinitions: [
      {
        AttributeName: 'projectId',
        AttributeType: 'S',
      },
      {
        AttributeName: 'username',
        AttributeType: 'S',
      },
    ],
    KeySchema: [
      {
        AttributeName: 'projectId',
        KeyType: 'HASH',
      },
      {
        AttributeName: 'username',
        KeyType: 'RANGE',
      },
    ],
  },
},
```

This code defines three DynamoDB tables.

The first one `Tasks` will store the tasks of our application. `Projects` will keep track of projects, and `ProjectUsers` will store the relationship between projects and users.

Note that we don't have a `Users` table. Users live in Cognito, and we won't need to store them in DynamoDB in this project.

## Data Sources

We now have our data stores defined, but we still need to link them to our GraphQL API.

To do so, AWS AppSync uses Data Sources. Data Sources are like adapters that connect to the different data stores. 

Since we have three DynamoDB tables, we will need 3 data source definitions of type `AMAZON_DYNAMODB`. Each references its corresponding DynamoDB table which we defined in the previous section.

Open `definitions/appsync.ts` and inside `dataSources`, add the following code:

```tsx showLineNumbers
tasks: {
  type: 'AMAZON_DYNAMODB',
  config: {
    tableName: { Ref: 'Tasks' },
  },
},
projects: {
  type: 'AMAZON_DYNAMODB',
  config: {
    tableName: { Ref: 'Projects' },
  },
},
projectUsers: {
  type: 'AMAZON_DYNAMODB',
  config: {
    tableName: { Ref: 'ProjectUsers' },
  },
},
```

For more details about Data Source definitions, check the [documentation](https://github.com/sid88in/serverless-appsync-plugin/blob/master/doc/dataSources.md).


### Lesson 4: Subscription


# Subscriptions

AWS AppSync comes with built-in real-time pub/sub capabilities. We will use it to allow our users to receive notifications when a task is updated, or assigned.

In GraphQL and AppSync, a subscription is a websocket connection that users can subscribe to and receive messages in real time. Subscriptions are triggered in response to a mutation.

## Task Updated

Open the schema file (`schema/schema.graphql`), and add the following code.

```graphql
type Subscription {
  onUpdateTask(id: ID!): Task @aws_subscribe(mutations: ["updateTask"])
}
```

Here, we are creating a new `Subscription` type and we introduce the `onTaskUpdated` subscription. The subscription takes an argument (`id`) which will take the id of the task to listen for changes.

We also use the AWS AppSync directive `@aws_subscribe` to specify which mutation triggers the subscription. Here, it's `updateTask`. 

This means that each time a user will invoke the `updateTask` mutation on a task, any user listening for changes on it will be notified. With AWS AppSync, you do not need to do anything other than using the directive.

Let's try it. First, we need to deploy our changes.

```bash
npx sls deploy
```

When it's done, try to execute the following subscription. Don't forget to change the task `id` to the id of one of your tasks.

```graphql
subscription OnTaskUpdated {
  onUpdateTask(id: "1c4b479e-62b2-41ca-a3ad-594cbc506604") {
    id
    title
    description
    priority
    status
    createdAt
    updatedAt
  }
}
```

Then, from another tab, invoke the following mutation using your admin user

```graphql
mutation UpdateTask {
  updateTask(
    input: {
      id: "1c4b479e-62b2-41ca-a3ad-594cbc506604"
      title: "My Updated Task 1"
    }
  ) {
    id
    title
    description
    priority
    status
    createdAt
    updatedAt
  }
}
```

If you come back to the tab where the subscription is running, you should see an incoming message with the task that was updated.

## Task Assigned Subscriptions

We just saw how to create a simple subscription. However, sometimes you need advanced use cases. AWS AppSync comes with a feature called [enhanced subscription filtering](https://docs.aws.amazon.com/appsync/latest/devguide/aws-appsync-real-time-enhanced-filtering.html). It allows you to create subscriptions with advanced filters.

Let's add a new subscription to illustrate this use case. Add the `onTaskAssigned` subscription in `schema/schema.graphql`.

```graphql
type Subscription {
  onUpdateTask(id: ID!): Task @aws_subscribe(mutations: ["updateTask"])
  // highlight-start
  onTaskAssigned(minPriority: Int): Task
    @aws_subscribe(mutations: ["createTask"])
  // highlight-end
}
```

Enhanced filtering requires some custom code that we write in a resolver. However, this resolver does not need to access any data source, it is just there to configure the filtering. Luckily, AWS AppSync allows us to do so with a special kind of data source: `NONE`. _none_ is a special kind of data source that do not connect to any store.

Let's create a _none_ data source. In `definitions/appsync.ts`, add the following code inside `dataSources`

```tsx
none: {
  type: 'NONE',
},
```

And, in `resolvers`

```tsx
'Subscription.onTaskAssigned': {
  dataSource: 'none',
  kind: 'UNIT',
  code: 'src/resolvers/Subscription.onTaskAssigned.ts',
},
```

Finally, create the `src/resolvers/Subscription.onTaskAssigned.ts` file

```tsx showLineNumbers
import {
  Context,
  SubscriptionFilterObject,
  extensions,
} from '@aws-appsync/utils';
import { SubscriptionOnTaskAssignedArgs, Task } from '../types/schema';
import { isCognitoIdentity } from '../utils';

export const request = (ctx: Context<SubscriptionOnTaskAssignedArgs>) => {
  return {};
};

export const response = (ctx: Context<SubscriptionOnTaskAssignedArgs>) => {
  if (!isCognitoIdentity(ctx.identity)) {
    util.unauthorized();
  }

  const filter: SubscriptionFilterObject<Task> = {
    assignees: {
      contains: ctx.identity.username,
    },
  };

  if (ctx.args.minPriority) {
    filter.priority = {
      ge: ctx.args.minPriority,
    };
  }

  extensions.setSubscriptionFilter(util.transform.toSubscriptionFilter(filter));

  return ctx.result;
};
```

Let's pause to analyze what is going on.

In the _request_ handler, we are checking that the current request comes from a Cognito user (lines 14-16). This is because we want the current user to receive notifications for tasks assigned to himself. 

Requests coming from non-users (e.g. API keys) should not be allowed to use this subscription, and it would also not make sense.

Then, we start by creating a filter rule (18-22). The rule specifies that the task's `assignees` should contain the current user's username for it to apply.

Finally, our subscription has an optional `minProperty` argument. If the argument is present, we use it to add a rule that requires the task's priority to be of at least the specified value (line 26). 

Tasks with a lower priority would not invoke the subscription. This can be used by users to avoid receiving unnecessary noisy notifications.

We finish by applying the subscription filter with the `extensions.setSubscriptionFilter()` helper function on line 30.

Let's deploy again and test.

```bash
npx sls deploy
```

With your standard user (non admin), try to execute the following subscription.

```graphql
subscription OnTaskAssigned {
  onTaskAssigned(minPriority: 5) {
    id
    title
    description
    priority
    status
    createdAt
    updatedAt
  }
}
```

Then, invoke the `createTask` Mutation with your admin user. Change the `assignees` to match your non-admin user.

```graphql
mutation CreateTask {
  createTask(
    input: {
      title: "Task 99"
      description: "My first task"
      priority: 3
      status: TODO
      projectId: "1d49e592-e489-43cc-8ce5-d7d99a731cc4"
      assignees: ["ben"]
    }
  ) {
    id
    title
    description
    priority
    status
    createdAt
    updatedAt
    assignees
  }
}
```

Try several combinations of `assignees`, `priority` . Also try to change or remove the `minPriority` argument from the subscription. Observe how and when the subscription receives the notification and make sure it behaves as expected.

### Lesson 5: User Privileges and Authorization


# Authorization


## Limit Tasks to Project Users

Now that only admins can perform write operations on tasks, we would also like to prevent users from seeing tasks of projects they are not in.

In this case, we cannot use a directive. Projects and user associations live in DynamoDB, so we will have to write the logic ourselves.

To achieve our goal, we can use pipeline resolvers.

Pipeline resolvers are a special kind of resolver that allow for connecting to more than one data source. Each pipeline resolver is composed of up to 10 functions that are executed in a sequence.

![graph_1](https://d14x58xoxfhz1s.cloudfront.net/8176d76e-330d-40f4-ac71-501f263f995d)

In our case, we want to first fetch a Task, extract its `projectId`, and then verify that the user is in that project by looking in the `ProjectUsers` table if a relation record exists. 

If the record exists, it means that the user is in the project. If not, we disallow the request by throwing an `unauthorized` error.


![mermaid](https://d14x58xoxfhz1s.cloudfront.net/717cf3e8-a2ed-4991-981e-1637b650b22d)


Open the `src/definitions/appsync.ts` file, and add the following code inside the `appSync` definition object.

```tsx
pipelineFunctions: {
  authorizeUser: {
    dataSource: 'projectUsers',
    code: 'src/resolvers/authorizeUser.ts',
  },
},
```

This defines a pipeline function. It uses the `projectUsers` data source which connects to the DynamoDB table of the same name.

Now, create the following file `src/resolvers/authorizeUser.ts`

```tsx showLineNumbers
import { Context, util, runtime } from '@aws-appsync/utils';
import { get } from '@aws-appsync/utils/dynamodb';
import { DBProjectUser } from '../types/db';
import { isCognitoIdentity } from '../utils';

export const request = (ctx: Context) => {
  // highlight-start
  if (!isCognitoIdentity(ctx.identity)) {
    util.unauthorized();
  }
  // highlight-end

  // highlight-start
  if (ctx.identity.groups?.includes('Admins')) {
    runtime.earlyReturn(ctx.prev.result);
  }
  // highlight-end

  return get<DBProjectUser>({
    key: {
      projectId: ctx.prev.result.projectId,
      username: ctx.identity.username,
    },
  });
};

export const response = (ctx: Context) => {
  // highlight-start
  if (!ctx.result) {
    util.unauthorized();
  }

  return ctx.prev.result;
  // highlight-end
};
```

A pipeline resolver function looks exactly like a unit resolver. In the above code, we generate a `GetItem` request to DynamoDB by using the `projectId` from the task (`ctx.prev.result.projectId`) and the `username` of the current user.

We also do a few more pre-checks:

On lines 7-9, we use `isCognitoIdentity`, a custom function that I created. It serves two purposes.

1. It makes sure that the current request is invoked using a Cognito user. Since, AppSync supports more than one authorizer, we need to make sure that the current request is authorized by Cognito before we proceed. If it's not the case, we always reject the request with `unauthorized()`

2. It serves as a TypeScript type guard by making sure that `ctx.identity` is of type `AppSyncIdentityCognito`. This avoids TypeScript from complaining that `username` might not exist.

On lines 11-13, we also check that the current user is not in the `Admins` group. If the user is an admin, we always want the request to proceed and we don't care if the user belongs to the project or not. 

For that, we make use of the `runtime.earlyReturn()` function. This function allows us to short-circuit the current resolver invocation and **skip** the data source request. It means that the `GetItem` request to DynamoDB will not happen at all and the _response_ handler is also not called. 

The value in passed to `earlyReturn()` is the value passed on to the next resolver in the pipeline, or as the GraphQL response if it's the last one in line.

Finally, on line 24-26, we check if an item was returned from DynamoDB. If no result is found, the user does not belong to the project, so we return an `unauthorized` error. Otherwise, we return `ctx.prev.result`. 

In other words, we return the result from the _previous_ resolver, which is our “Get Task” resolver. This is what will be returned to the client.

We now have our authorizer function, but we still need to use it.

Update the `getTask` and `listTasks` resolvers `definitions/appsync.ts` as follow:

```tsx showLineNumbers
'Query.getTask': {
  kind: 'PIPELINE',
  functions: [
    {
      dataSource: 'tasks',
      code: 'src/resolvers/Query.getTask.ts',
    },
    'authorizeUser',
  ],
},
'Query.listTasks': {
  kind: 'PIPELINE',
  code: 'src/resolvers/Query.listTasks.ts',
  functions: [
    'authorizeUser',
    {
      dataSource: 'tasks',
      code: 'src/resolvers/listTasks.ts',
    },
  ],
},
```

What we did is to transform the unit resolvers into pipeline resolvers, and we introduced the `authorizeUser` pipeline function.

Under `getTask`, the authorization happens after fetching the task, because we first need the task entity so we can read the `projectId` from it. 

On the other hand, the `listTasks` query, comes with the `projectId` in `ctx.args.id`, so we immediately check the authorization before we even try to read the tasks from the table.

We also need to rename `src/resolvers/Query.listTasks.ts` to `src/resolvers/listTasks.ts` , and create a new `src/resolvers/Query.listTasks.ts` with the following content:

```tsx showLineNumbers
import { Context } from '@aws-appsync/utils';
import { QueryListTasksArgs } from '../types/schema';

export const request = (ctx: Context<QueryListTasksArgs>) => {
  return {
    projectId: ctx.args.projectId,
  };
};

export const response = (ctx: Context) => {
  return ctx.result;
};
```

What happens here is that we created a _before pipeline resolver_ (`request`). A _before pipeline resolver_ does not connect to any data source, but is there to pre-process the incoming request from GraphQL. 

It is executed before the very first function in the pipeline. We use it in order to extract the project id from the arguments, and pass it to the next resolver (`authorizeUser`).

There is also an _after pipeline resolver_ (`response`) that happens after all the functions been executed. Here, we just return the result from the last function.

To learn more about pipeline resolvers, check the [documentation](https://docs.aws.amazon.com/appsync/latest/devguide/resolver-reference-overview-js.html#anatomy-of-a-pipeline-resolver-js).


There are two ways to define a pipeline function in the serverless framework. One is to define it in `pipelineFunctions`, which is what we did earlier with `authorizeUser`. This is a way to create re-useable functions.

The other one is to define it inline in the `functions` array. This is useful if the function is unique and you know it will not be reused. This is what we did with `src/resolvers/listTasks.ts`



As a rule of thumb, I highly recommend to always create pipeline resolvers, even if you only have one function in the pipeline. This makes it a lot easier to add a new function without doing complex refactoring if you need to later.

```tsx
'Query.listTasks': {
  kind: 'PIPELINE',
  functions: [
    {
      dataSource: 'tasks',
      code: 'src/resolvers/getTask.ts',
    },
  ],
},
```



Now, deploy the API again.

```bash
npx sls deploy
```

Use your non-admin user to test the `getTask` and `listTasks` operations.

```graphql
query ListTasks {
  # Change the project id with your own project id
  listTasks(projectId: "1d49e592-e489-43cc-8ce5-d7d99a731cc4") {
    items {
      id
      title
      description
      priority
      status
      createdAt
      updatedAt
      assignees
    }
    nextToken
  }
}
```

You should get an error.

```json
{
  "data": null,
  "errors": [
    {
      "path": ["listTasks"],
      "data": null,
      "errorType": "Unauthorized",
      "errorInfo": null,
      "locations": [
        {
          "line": 2,
          "column": 3,
          "sourceName": null
        }
      ],
      "message": "Not Authorized to access listTasks on type Query"
    }
  ]
}
```

Switch to your admin user, and use `addUserToProject` mutation to add that user to the project.

```graphql
mutation AddUserToProject {
  addUserToProject(
    input: {
      projectId: "1d49e592-e489-43cc-8ce5-d7d99a731cc4"
      username: "ben"
    }
  ) {
    username
    createdAt
  }
}
```

Then switch back to the non-admin user again and try executing the `getTask` and `listTasks` queries again. This time, you should get access to the resources.

### Lesson 6: Admin Privileges and Authorization


# Authorization

## Limit Write Privileges to Admins

In our current situation, any user is capable of creating, updating and deleting tasks and projects. But what if we wanted to only allow some users (i.e. admins) to execute those actions?

Open the schema file: `schema/schema.graphql`. Change the `Mutation` definition as follows.

```graphql
type Mutation {
  createTask(input: CreateTaskInput!): Task!
    @aws_auth(cognito_groups: ["Admins"])
  updateTask(input: UpdateTaskInput!): Task!
    @aws_auth(cognito_groups: ["Admins"])
  deleteTask(id: ID!): Task! @aws_auth(cognito_groups: ["Admins"])
  createProject(input: CreateProjectInput!): Project!
    @aws_auth(cognito_groups: ["Admins"])
  updateProject(input: UpdateProjectInput!): Project!
    @aws_auth(cognito_groups: ["Admins"])
  deleteProject(id: ID!): Project! @aws_auth(cognito_groups: ["Admins"])
  addUserToProject(input: AddUserToProjectInput!): ProjectUser!
    @aws_auth(cognito_groups: ["Admins"])
}
```

Here, we make use of the `@aws_auth` directive, which specifies that only users in the Cognito `Admin` group are allowed to call these mutations.

Finally, deploy the API again.

```bash
npx sls deploy
```

When the deployment is done, try to create, update or delete a Task. You should observe that it fails with an `Unauthorized` error.

```json
{
  "data": null,
  "errors": [
    {
      "path": ["createTask"],
      "data": null,
      "errorType": "Unauthorized",
      "errorInfo": null,
      "locations": [
        {
          "line": 2,
          "column": 3,
          "sourceName": null
        }
      ],
      "message": "Not Authorized to access createTask on type Mutation"
    }
  ]
}
```

Now, let's create a new group in Cognito named `Admins`.

Go to the [Amazon Cognito AWS console](https://us-east-1.console.aws.amazon.com/cognito/v2/idp/user-pools?region=us-east-1), and select the user pool relative to our API.

Under _Group_, click the _Create Group_ button. Give it a name: `Admins`, and hit _save._

Create a new user, using the same two commands as in the [previous section](https://www.educloud.academy/content/242df9c1-7aec-49ac-a4d1-4646fe44a595/46f3f1e5-e032-4517-ae41-8543366a5c35/22dcac25-9b9e-455d-b536-3305cf3b3750/).

Finally, add the user to the group using the AWS console. Open the user and click on _Add user to group_. Pick the `Admins` group.

Then, try to log in using your new user, and execute the mutation again. This time, you should be allowed to perform the action.


### Lesson 7: Define the Stack

# Defining the Stack

We will start by defining the basic resources for our API: the API itself and the Cognito User Pool.

![AppSync API and Cognito User Pool](https://d14x58xoxfhz1s.cloudfront.net/1762be31-aa03-4e98-98b4-1f5a55b6d92b)

## AppSync API

Our stack uses the [serverless-appsync-plugin](https://github.com/sid88in/serverless-appsync-plugin). Let's start by adding the required definitions for our API. We will give our API a name, a schema and a default authentication method.

Open the `definitions/appsync.ts` file and add the following code under _`1.1. Define the AppSync API`_

```tsx 
name: 'AppSync Workshop',
schema: 'schema/schema.graphql',
authentication: {
  type: 'AMAZON_COGNITO_USER_POOLS',
  config: {
    userPoolId: {
      Ref: 'CognitoUserPool',
    },
  },
},
dataSources: {},
resolvers: {},
```

## Cognito User Pool

Our API uses a Cognito User Pool as its default authorizer (lines 3-10 in the API definition). Let's define it too.

In `definitions/cognito.ts`, add this code.

```tsx 
// 1.2. Define the Cognito User Pool
CognitoUserPool: {
  Type: 'AWS::Cognito::UserPool',
  Properties: {
    UserPoolName: 'AWS AppSync Workshop User Pool',
    AutoVerifiedAttributes: ['email'],
  },
},
CognitoUserPoolClient: {
  Type: 'AWS::Cognito::UserPoolClient',
  Properties: {
    ClientName: 'AWS AppSync Workshop Client',
    UserPoolId: {
      Ref: 'CognitoUserPool',
    },
    ExplicitAuthFlows: [
      'ALLOW_USER_PASSWORD_AUTH',
      'ALLOW_USER_SRP_AUTH',
      'ALLOW_REFRESH_TOKEN_AUTH',
    ],
  },
},
```

This will create a Cognito User Pool and a User Pool Client.

## First Deployment

We have defined our API and Cognito user pool. It's now time for our first deployment.

Run the following command.

```shell
npx sls deploy
```

If everything went well, you should see an output similar to this:

```shell
Deploying appsync-typescript-workshop to stage dev (us-east-1)

✔ Service deployed to stack appsync-typescript-workshop-dev (92s)

appsync endpoints:
  graphql: https://xbtmamhhkzfm7oudu7z4mvk5ti.appsync-api.us-east-1.amazonaws.com/graphql
  realtime: wss://xbtmamhhkzfm7oudu7z4mvk5ti.appsync-realtime-api.us-east-1.amazonaws.com/graphql
```

The output also gives us information about the deployed API, such as its endpoints. You might want to copy the `graphql` endpoint and keep it somewhere for later.

## Module 3: Conclusion

### Lesson 1: Conclusion



# Conclusion & Clean Up

We have now reached the end of this workshop. I truly hope that you have learned something. Your feedback is important, so please don't hesitate to send me a message if you have any issue or have any questions or comments. 

You can reach me at benoit@appsync.wtf

I encourage you to keep practicing and experimenting with AWS AppSync. There is a lot more you can do. You can use this project as a starting point if you want.

Before cleaning everything up, have a look at the final solution and make sure you understand everything. You can also find the [solution on Github](https://github.com/bboure/appsync-typescript-workshop/tree/solution). 

To clean up everything we just did, you can run the following command.

```bash
npx sls remove
```

## Module 4: Introduction

### Lesson 1: What is Appsync ?

## What is AWS AppSync?

AppSync is a fully-managed and serverless service from AWS that allows developers to build scalable GraphQL APIs in no time without having to worry about maintaining servers. 

AWS AppSync seamlessly integrates with other AWS services such as Amazon DynamoDB, AWS Lambda, Amazon EventBridge, Amazon Aurora, Amazon OpenSearch and Amazon Cognito.

![AWS AppSync overview](https://d14x58xoxfhz1s.cloudfront.net/2a1f8273-ff68-4437-891b-ccb4bb05d256)

### Lesson 2: Prerequisites

## Prerequisites

To follow this workshop, you will need:

- [An AWS account](https://portal.aws.amazon.com/billing/signup#/start/email)
- Basic understanding of GraphQL and the Schema Definitions Language (SDL)
- Basic knowledge about AWS and its services (i.e. DynamoDB, Cognito)
- Some background with TypeScript

High-level understanding the [Serverless Framework](https://www.serverless.com/) might also be useful.

Ready? Let's get started.

### Lesson 3: What will we build ?

## What Will we Build?

We will create a collaborative task management system where users can create projects and tasks, and receive notifications and updates in real-time. 

We will use AWS AppSync to build a GraphQL API with pub/sub capabilities as well as its built-in authentication and authorization features and Amazon Cognito to control who can access the API and which operations they can do. 

Finally, we will also use Amazon DynamoDB as our main data store.

![Project Overview](https://d14x58xoxfhz1s.cloudfront.net/5bee9a20-c3e6-4613-8d7b-5bf7f0e03d07)

For reference, here are the GraphQL types that will serve as our base.

```graphql
type Task {
  id: ID!
  title: String!
  description: String!
  priority: Int!
  status: Status!
  project: Project!
  assignees: [ID!]!
  createdAt: AWSDateTime!
  updatedAt: AWSDateTime!
}

type Project {
  id: ID!
  name: String!
  description: String!
  createdAt: AWSDateTime!
  updatedAt: AWSDateTime!
}
```




### Lesson 4: GraphQL vs REST?

## GraphQL vs REST

GraphQL is an open-source data query and manipulation language for APIs and a query runtime engine. It was created by Facebook in 2012 before being made publicly available in 2015.

GraphQL and REST are two ways to create APIs, however they differ in a few ways.

**Reads and Writes**

REST uses verbs to communicate which operation the client wants to perform (e.g. `GET` for reads, and `PUT`, `POST` or `DELETE` for writes).

GraphQL uses _Queries_ for read operations and _Mutations_ for writes. In addition to that, it utilizes _Subscriptions_ for real-time communication.

**Underfetching and Overfetching**

In REST, **underfetching** occurs when multiple requests are needed to gather all the required data. For example, if you need to fetch a user and his/her last 10 orders, you might need to send the following two requests: `GET /user/123` and `GET /orders?userId=123&limit=10&order=DESC`

Sometimes, those requests might even need to be consecutive. i.e. if the second request requires a value coming from the first one. This leads to increased latency and network overhead.

REST APIs also often send more data than necessary. In our previous example, you might only need the `name` , `avatar` and `email` of the user, but not the `address` and `biography`. REST usually does not offer control on that and returns all the available fields. This is called **overfetching** and it increases the payload size unnecessarily.

GraphQL tries to solve those two issues as it allows the client to query all the necessary data in a single query, and omit what it doesn't need.

Here is what an equivalent GraphQL request might look like.

```graphql
query {
  # Get a user
  # Only retrieve the name, avatar and email
  getUser(id: "123") {
    id
    name
    avatar
    email
    # last 10 orders of the user
    # Only retrieve the id and date
    orders(limit: 10, order: "DESC") {
      id
      date
    }
  }
}
```

**Real-time**

REST does not have any real-time capability. If you need pub/sub for your API, you will need to build a complete different API (i.e. WebSocket) in parallel.

As mentioned earlier, GraphQL supports *Subscriptions*. You will learn about subscriptions during this workshop.

### Lesson 5: Will it Cost me Anything ?

## Will it Cost me Anything?

This workshop involves deploying several resources into your own AWS account. While most of those services have a generous free tier, you might incur some charges. However those services are inexpensive at this scale and cost should remain moderate.

When this workshop is finished, we will also learn how to clean up and remove all the created resources to suppress any possible charges.

