import launchflow as lf
import os

dst_path = os.path.join(os.getcwd(), "dist")

backend_bucket = lf.gcp.BackendBucket(
    name="tanke-react-static-site",
    local_folder_path=dst_path,
    force_destroy=True,
)

