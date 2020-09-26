import { Trans } from "@lingui/macro"
import React from "react"
import * as Yup from "yup"
import { useSettingsContext } from "../../../Context"
import {
  CardAlert,
  CardBody,
  Field,
  FieldError,
  Form,
  FormFooter,
  Input,
  ThreadTitleValidationError,
} from "../../../UI"
import { IThread } from "../Thread.types"
import ThreadRootError from "../ThreadRootError"
import useEditThreadTitleMutation from "./useEditThreadTitleMutation"

interface IThreadHeaderTitleEditFormProps {
  thread: IThread
  close: () => void
}

interface IFormValues {
  title: string
}

const ThreadHeaderTitleEditForm: React.FC<IThreadHeaderTitleEditFormProps> = ({
  close,
  thread,
}) => {
  const { threadTitleMaxLength, threadTitleMinLength } = useSettingsContext()

  const {
    data,
    loading,
    editThreadTitle,
    error: graphqlError,
  } = useEditThreadTitleMutation(thread)

  const EditThreadTitleSchema = Yup.object().shape({
    title: Yup.string()
      .required("value_error.missing")
      .min(threadTitleMinLength, "value_error.any_str.min_length")
      .max(threadTitleMaxLength, "value_error.any_str.max_length")
      .matches(/[a-zA-Z0-9]/, "value_error.thread_title"),
  })

  return (
    <Form<IFormValues>
      id="thread_header_edit_form"
      defaultValues={{ title: thread.title }}
      disabled={loading}
      validationSchema={EditThreadTitleSchema}
      onSubmit={async ({ clearError, setError, data: { title } }) => {
        clearError()

        try {
          const result = await editThreadTitle(title)
          const { errors } = result.data?.editThreadTitle || {}

          if (errors) {
            errors?.forEach(({ location, type, message }) => {
              const field = location.join(".") as "title"
              setError(field, type, message)
            })
          } else {
            close()
          }
        } catch (error) {
          // do nothing when editThreadTitle throws
          return
        }
      }}
    >
      <ThreadRootError
        graphqlError={graphqlError}
        dataErrors={data?.editThreadTitle.errors}
      >
        {({ message }) => <CardAlert>{message}</CardAlert>}
      </ThreadRootError>
      <CardBody className="thread-header-edit-form">
        <Field
          name="title"
          input={<Input />}
          error={(error, value) => (
            <ThreadTitleValidationError
              error={error}
              value={value.trim().length}
              min={threadTitleMinLength}
              max={threadTitleMaxLength}
            >
              {({ message }) => <FieldError>{message}</FieldError>}
            </ThreadTitleValidationError>
          )}
        />
        <FormFooter
          loading={loading}
          submitText={<Trans id="save">Save</Trans>}
          onCancel={close}
        />
      </CardBody>
    </Form>
  )
}

export default ThreadHeaderTitleEditForm