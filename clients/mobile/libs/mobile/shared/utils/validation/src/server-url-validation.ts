import { i18n } from '@ronas-it/react-native-common-modules/i18n';
import * as Yup from 'yup';
import { isValidServerUrl } from '@open-webui-react-native/shared/utils/config';
export const serverUrlValidator = (): Yup.StringSchema =>
  Yup.string()
    .trim()
    .test('server-url', i18n.t('SHARED.VALIDATION.TEXT_INVALID_URL'), (value) =>
      !value || isValidServerUrl(value));
