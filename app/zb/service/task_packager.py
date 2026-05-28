from common.util.export import File, dir_object, logger

from ..model.constants import Fp


class TaskPackager:
    def package(self, root: File, instance_json: File):
        z = root.extend(".zip").remove()
        z.zip(targets=[root.child(d) for d in dir_object(Fp, str)] + [instance_json])
        logger.info(z)
        return z