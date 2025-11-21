import numpy as np
from typing import TypeVar
from typing import NamedTuple
from dataclasses import dataclass
from scipy.spatial.transform import Rotation, Slerp

# This is solely for type hinting the interpolate method that can take another Pose as an argument
Pose_T = TypeVar("Pose_T", bound="Pose")

class Pose(NamedTuple):
    '''
    Position is represented as a 3D numpy array (x, y, z).
    Rotation is represented as a scipy Rotation object (quaternion internally).
    '''
    position: np.ndarray
    rotation: Rotation

    @staticmethod
    def identity():
        return Pose(np.zeros(3), Rotation.identity())

    def to_dict(self):
        return {
            "position": self.position.tolist(),
            "rotation_quat": self.rotation.as_quat().tolist(),
        }

    @staticmethod
    def from_dict(d):
        return Pose(
            position=np.array(d["position"]),
            rotation=Rotation.from_quat(d["rotation_quat"]),
        )

    def interpolate(self, other: Pose_T, proportion: float):
        """
        Interpolates or extrapolates between two poses.
        "proportion" is effectively a bias between A and B. I
            If proportion is 0, returns self. If proportion is 1, returns other. If proportion is somewhere in between, this function will return something in between.
            If proportion < 0 or > 1, we extrapolate in the direction of self (if < 0) or other (if > 1)
                For example, if proportion is -1, we go 1 unit "under" A (one unit is the delta between self and other)
        """
        new_pos = self.position + proportion * (other.position - self.position)
        if 0 <= proportion <= 1:
            return Pose(
                position=new_pos,
                rotation=Slerp(  # This interpolates two rotations. For complicated math reasons, it isn't as simple as interpolating vectors.
                    [0, 1], Rotation.concatenate([self.rotation, other.rotation])
                )(proportion),
            )
        # extrapolate
        rel_rot = other.rotation * self.rotation.inv()
        return Pose(
            position=new_pos,
            rotation=(  # This extrapolates the rotation beyond 'self.rotation' in the direction of 'other.rotation' by 'proportion'
                # No slerp here because we can scale directly for extrapolation
                Rotation.from_rotvec(rel_rot.as_rotvec() * proportion) * self.rotation
            ),
        )

    def __eq__(self, other: Pose_T):
        return (
            np.allclose(self.position, other.position)
            and self.rotation == other.rotation
        )