import * as React from 'react';
import { cn } from '@shared/lib/utils';

export interface InputProps extends React.ComponentProps<'input'> {
  errorMessage?: string;
  reserveErrorSpace?: boolean;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    { id, className, type, errorMessage, reserveErrorSpace = false, ...props },
    ref
  ) => {
    const autoId = React.useId();
    const inputId = id ?? autoId;
    const errorId = `${inputId}-error`;

    const hasError = !!errorMessage;
    const showErrorContainer = hasError || reserveErrorSpace;

    return (
      <div className="flex flex-col gap-1">
        <input
          id={inputId}
          ref={ref}
          type={type}
          data-slot="input"
          aria-invalid={hasError}
          aria-errormessage={hasError ? errorId : undefined}
          aria-describedby={hasError ? errorId : undefined}
          className={cn(
            'file:text-foreground placeholder:text-muted-foreground ' +
              'selection:bg-primary selection:text-primary-foreground ' +
              'dark:bg-input/30 border-input flex h-9 w-full min-w-0 ' +
              'rounded-md border bg-transparent px-3 py-1 text-base ' +
              'shadow-xs transition-[color,box-shadow] outline-none ' +
              'file:inline-flex file:h-7 file:border-0 file:bg-transparent ' +
              'file:text-sm file:font-medium disabled:pointer-events-none ' +
              'disabled:cursor-not-allowed disabled:opacity-50 md:text-sm',
            'focus-visible:border-ring focus-visible:ring-ring/50 ' +
              'focus-visible:ring-[3px]',
            'aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 ' +
              'aria-invalid:border-destructive',
            className
          )}
          {...props}
        />

        {showErrorContainer && (
          <p
            id={errorId}
            role="alert"
            className={cn(
              'text-sm text-destructive mt-1',
              !hasError && 'invisible'
            )}
          >
            {/* if no real error, emit a non-breaking‐space to keep the <p> height */}
            {hasError ? errorMessage : '\u00A0'}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
