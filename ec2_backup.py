from datetime import datetime
import boto3


def lambda_handler(event, context):
    
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
            for region in ec2_client.describe_regions()['Regions']]
            
    for region in regions:
        
        print('Instances in EC2 Region {0}:'.format(region))
        
        ec2 = boto3.resource('ec2', region_name=region)
        
        instances = ec2.instances.filter(
                    Filters=[
                        {'Name': 'tag:Env', 'Values': ['Prod']}
            ]
        )
            
        # ISO 8601 timestamp, i.e. 2022-11-05-22-01-01
        timestamp = datetime.utcnow().replace(microsecond=0).isoformat()
        
        for i in instances.all():
            for v in i.volumes.all():
                
                describe = 'Backup of {0}, volume {1}, created {2}'.format(
                    i.id, v.id, timestamp)
                print(describe)
                
                snapshot = v.create_snapshot(Description=describe)
                
                print("Created snapshot:", snapshot.id)