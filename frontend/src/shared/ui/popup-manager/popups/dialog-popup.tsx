import {
  Dialog,
  DialogContent,
  DialogTitle,
} from '@/shared/components/ui/dialog';
import { InjectablePopupProps } from '../popup-props';
import { Button, ButtonVariant } from '@/shared/components/ui/button';
import { Input } from '@/shared/components/ui/input';
import { useCallback, useState } from 'react';

type InputId = string;

type DialogPopupProps = {
  title: string;
  description?: string;
  inputs?: {
    id: InputId;
    label: string;
    value: string;
    validate?: (
      value: string
    ) => { valid: true } | { valid: false; error: string };
    resetErrorOnChange?: boolean;
  }[];
  buttons?: {
    text: string;
    onClick: (inputValues: Record<string, string>) => void;
    variant?: ButtonVariant;
    needsInputsValidation?: boolean;
  }[];
};

export const DialogPopup = (props: DialogPopupProps & InjectablePopupProps) => {
  const [inputValues, setInputValues] = useState<Record<InputId, string>>(
    (props.inputs ?? []).reduce(
      (acc, input) => {
        acc[input.id] = input.value;
        return acc;
      },
      {} as Record<string, string>
    )
  );

  const [inputsErrors, setInputsErrors] = useState<
    Record<InputId, string | undefined>
  >({});
  const validateFields: () => Record<InputId, string | undefined> =
    useCallback(() => {
      const newErrorsState: Record<InputId, string | undefined> = {};
      for (const input of props.inputs ?? []) {
        if (input.validate) {
          const result = input.validate(inputValues[input.id]);
          Object.assign(newErrorsState, {
            [input.id]: result.valid ? undefined : result.error,
          });
        }
      }
      setInputsErrors(newErrorsState);
      return newErrorsState;
    }, [inputValues, props.inputs]);

  const anyInputHasError = useCallback(
    (errors: Record<InputId, string | undefined>) => {
      return Object.values(errors).some((error) => !!error);
    },
    []
  );

  return (
    <Dialog open={props.isOpen} onOpenChange={props.onOpenChange}>
      <DialogTitle>{props.title}</DialogTitle>
      <DialogContent className="w-[511px]">
        <div className="text-base font-semibold">{props.title}</div>
        {props.description && <div>{props.description}</div>}

        {props.inputs?.length && (
          <div className="flex flex-col gap-2">
            {props.inputs.map((inputProps) => (
              <Input
                key={inputProps.id}
                value={inputValues[inputProps.id]}
                errorMessage={inputsErrors[inputProps.id]}
                reserveErrorSpace={true}
                onChange={(e) => {
                  if (inputProps.resetErrorOnChange) {
                    setInputsErrors((state) => ({
                      ...state,
                      [inputProps.id]: undefined,
                    }));
                  }
                  setInputValues({
                    ...inputValues,
                    [inputProps.id]: e.target.value,
                  });
                }}
              />
            ))}
          </div>
        )}

        {props.buttons?.length && (
          <div className="flex justify-end gap-2">
            {props.buttons.map((buttonProps) => (
              <Button
                key={buttonProps.text}
                variant={buttonProps.variant ?? 'outline'}
                onClick={() => {
                  if (buttonProps.needsInputsValidation) {
                    const errors = validateFields();
                    if (anyInputHasError(errors)) {
                      return;
                    }
                  }
                  buttonProps.onClick(inputValues);
                }}
              >
                {buttonProps.text}
              </Button>
            ))}
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
};
