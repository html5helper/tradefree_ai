from ai.core.data_event import Event
from ai.business.social2product.tasks import run_workflow

# Create event using the Event class
event = Event.get_event_template("social2product")
event["context"]["platform"] = "tiktok"

# Run the workflow
res = run_workflow.apply_async(args=(event,))
print("Trace ID:", res.id)