# Events API Deployment Guide

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured with credentials
3. **Python 3.12+** installed
4. **Node.js 18+** (for AWS CDK)

## Quick Deploy

### 1. Install AWS CDK (if not already installed)
```bash
npm install -g aws-cdk
```

### 2. Configure AWS Credentials
```bash
aws configure
```

### 3. Deploy the Stack
```bash
chmod +x deploy.sh
./deploy.sh
```

Or manually:
```bash
cd infrastructure
pip install -r requirements.txt
cdk bootstrap  # Only needed once per account/region
cdk deploy
```

## What Gets Deployed

- **DynamoDB Table**: `Events` table with `eventId` as partition key
- **Lambda Function**: Python 3.12 function running FastAPI via Mangum
- **API Gateway**: REST API with CORS enabled, publicly accessible

## Architecture

```
Client → API Gateway → Lambda (FastAPI) → DynamoDB
```

## API Endpoints

After deployment, you'll get an API URL like:
`https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/prod/`

### Available Endpoints:

- `GET /` - API info
- `GET /health` - Health check
- `POST /events/` - Create event
- `GET /events/` - List all events (optional: ?status_filter=active)
- `GET /events/{event_id}` - Get specific event
- `PUT /events/{event_id}` - Update event
- `DELETE /events/{event_id}` - Delete event

## Testing the API

### Create an Event
```bash
curl -X POST https://YOUR-API-URL/prod/events/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "AWS re:Invent 2025",
    "description": "Annual AWS conference",
    "date": "2025-12-01",
    "location": "Las Vegas, NV",
    "capacity": 50000,
    "organizer": "AWS",
    "status": "active"
  }'
```

### List Events
```bash
curl https://YOUR-API-URL/prod/events/
```

### Get Event by ID
```bash
curl https://YOUR-API-URL/prod/events/{event_id}
```

### Update Event
```bash
curl -X PUT https://YOUR-API-URL/prod/events/{event_id} \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

### Delete Event
```bash
curl -X DELETE https://YOUR-API-URL/prod/events/{event_id}
```

## Monitoring

- **CloudWatch Logs**: Check Lambda logs in CloudWatch
- **API Gateway Metrics**: Monitor request count, latency, errors
- **DynamoDB Metrics**: Track read/write capacity usage

## Cleanup

To remove all resources:
```bash
cd infrastructure
cdk destroy
```

## Cost Considerations

This deployment uses serverless services with pay-per-use pricing:
- **Lambda**: Free tier includes 1M requests/month
- **API Gateway**: Free tier includes 1M requests/month
- **DynamoDB**: Free tier includes 25GB storage and 25 RCU/WCU
- **CloudWatch**: Basic monitoring included

For typical development/testing, this should stay within free tier limits.

## Troubleshooting

### Lambda Timeout
If requests timeout, increase the timeout in `backend_stack.py`:
```python
timeout=Duration.seconds(60)
```

### CORS Issues
Update `ALLOWED_ORIGINS` environment variable in `backend_stack.py`:
```python
environment={
    "ALLOWED_ORIGINS": "https://yourdomain.com,https://anotherdomain.com"
}
```

### Permission Errors
Ensure your AWS credentials have permissions for:
- Lambda (create/update functions)
- API Gateway (create/update APIs)
- DynamoDB (create/update tables)
- IAM (create roles)
- CloudFormation (create/update stacks)
