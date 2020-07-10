package shellcuts.core.actions

import org.scalatest.{
  EitherValues,
  FlatSpec
}

class JumpAndFollowActionSpec extends FlatSpec with EitherValues {
  "posixFormat()" should "handle an empty argument list" in {
    val givenArguments = List()
    val expectedMessage = "could not format command, no argument provided"

    val producedMessage = JumpAndFollowAction.posixFormat(givenArguments)
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "handle a missing second argument" in {
    val givenArguments = List("argument")
    val expectedMessage = "could not format command, missing follow-up arguments"

    val producedMessage = JumpAndFollowAction.posixFormat(givenArguments)
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "handle multiple arguments" in {
    val givenArguments = List("argument1", "argument2")
    val expectedString = raw"cd 'argument1'; argument2"

    val producedString = JumpAndFollowAction.posixFormat(givenArguments)
    assert(expectedString == producedString.right.value)
  }

  it should "handle an argument with an apostrophe" in {
    val givenArguments = List("argu'ment1", "argument2")
    val expectedString = raw"cd 'argu'\''ment1'; argument2"

    val producedString = JumpAndFollowAction.posixFormat(givenArguments)
    assert(expectedString == producedString.right.value)
  }

  it should "handle an argument with Unicode" in {
    val givenArguments = List("argument1😀", "argument2")
    val expectedString = raw"cd 'argument1😀'; argument2"

    val producedString = JumpAndFollowAction.posixFormat(givenArguments)
    assert(expectedString == producedString.right.value)
  }
}
