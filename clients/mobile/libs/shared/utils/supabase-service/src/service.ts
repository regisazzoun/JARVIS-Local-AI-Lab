import { createClient, SupabaseClient } from '@supabase/supabase-js';
import { decode } from 'base64-arraybuffer';
import Constants from 'expo-constants';
import { SupabaseBucket, SupabaseTable } from './enums';
import { SubmitFeedbackAttachment, SubmitFeedbackRequest } from './models';

class SupabaseService {
  private client: SupabaseClient | undefined;

  public init(): void {
    const supabaseConfig = Constants.expoConfig?.extra?.supabase;

    this.client = undefined;
    const url = supabaseConfig?.url;
    const key = supabaseConfig?.publishableKey;
    if (typeof url !== 'string' || !url.trim() || typeof key !== 'string' || !key.trim()) return;
    try {
    this.client = createClient(url, key, {
      auth: {
        persistSession: false,
        autoRefreshToken: false,
        detectSessionInUrl: false,
      },
    });
    } catch {
      // Optional feedback configuration must not prevent a self-hosted client from starting.
      this.client = undefined;
    }
  }

  public get isAvailable(): boolean { return this.client !== undefined; }

  private requireClient(): SupabaseClient {
    if (!this.client) throw new Error('Feedback is unavailable in this build.');
    return this.client;
  }

  public async submit(request: SubmitFeedbackRequest): Promise<void> {
    this.requireClient();
    const attachmentPaths = request.attachments?.length
      ? await Promise.all(request.attachments.map((attachment, index) => this.uploadAttachment(attachment, index)))
      : [];

    const { error } = await this.requireClient().from(SupabaseTable.FEEDBACK).insert({
      email: request.email,
      message: request.message,
      platform: request.platform,
      app_version: request.appVersion,
      api_version: request.apiVersion,
      attachment_paths: attachmentPaths,
    });

    if (error) {
      throw error;
    }
  }

  private async uploadAttachment(attachment: SubmitFeedbackAttachment, index: number): Promise<string> {
    const fallbackFileName = attachment.mimeType?.startsWith('video/') ? 'video.mp4' : 'image.jpg';
    const path = `${Date.now()}-${index}-${attachment.fileName ?? fallbackFileName}`;

    const { error } = await this.requireClient().storage
      .from(SupabaseBucket.FEEDBACK_ATTACHMENTS)
      .upload(path, decode(attachment.base64), {
        contentType: attachment.mimeType,
      });

    if (error) {
      throw error;
    }

    return path;
  }
}

export const supabaseService = new SupabaseService();
