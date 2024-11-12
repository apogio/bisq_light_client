from abc import abstractmethod
from bisq.core.common.protocol.persistable.persistable_envelope import PersistableEnvelope
from bisq.core.common.protocol.proto_resolver import ProtoResolver
import proto.pb_pb2 as protobuf


class PersistenceProtoResolver(ProtoResolver):
    @abstractmethod
    def from_proto(self, proto: protobuf.PersistableEnvelope) -> PersistableEnvelope:
        pass