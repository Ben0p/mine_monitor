import { Deserializable } from './deserializable.model'

export class AlertModules implements Deserializable {
    location : string;
    ip : string;

    deserialize(input: any) {
        Object.assign(this, input);
        return this;
      }
  }