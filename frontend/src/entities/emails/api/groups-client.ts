import axios from "axios";
import { BaseApi } from "@/shared/api/base-api";
import { CreateGroupDto, CreateGroupResponseDto } from "../types";

export class GroupsApi extends BaseApi {
  async createGroup(payload: CreateGroupDto): Promise<CreateGroupResponseDto | undefined> {
    try {
      const res = await axios.post(`${this.baseUrl}/group`, payload);
      return res.data;
    } catch {
      return undefined;
    }
  }
}

export const groupsClient = new GroupsApi({
  baseUrl: 'api/proxy/main-api'
});


