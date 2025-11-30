import axios from "axios";
import { BaseApi } from "@/shared/api/base-api";
import { CreateGroupDto, CreateGroupResponseDto, EmailsGroupDto, EmailAnalysisDto } from "../types";

export class GroupsApi extends BaseApi {
  async createGroup(payload: CreateGroupDto): Promise<CreateGroupResponseDto | undefined> {
    try {
      const res = await axios.post(`${this.baseUrl}/group/`, payload);
      return res.data;
    } catch {
      return undefined;
    }
  }

  async getGroups(): Promise<EmailsGroupDto[] | undefined> {
    try {
      const res = await axios.get(`${this.baseUrl}/group`);
      return res.data;
    } catch {
      return undefined;
    }
  }

  async getGroupStatus(groupId: string): Promise<{ status: "Finished" | "Working" } | undefined> {
    try {
      const res = await axios.get(`${this.baseUrl}/group/status/${groupId}`);
      return res.data;
    } catch {
      return undefined;
    }
  }

  async getGroupAnalysis(groupId: string): Promise<{
    email_raw: { id: string; text: string };
    analysis: EmailAnalysisDto;
  }[] | undefined> {
    try {
      const res = await axios.get(`${this.baseUrl}/group/analysis/${groupId}`);
      return res.data;
    } catch {
      return undefined;
    }
  }
}

export const groupsClient = new GroupsApi({
  baseUrl: '/api/proxy/main-api'
});


