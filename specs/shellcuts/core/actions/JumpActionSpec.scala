package shellcuts.core.actions

import org.scalatest.{
  EitherValues,
  FlatSpec
}

class JumpActionSpec extends FlatSpec with EitherValues {
  "posixFormat()" should "handle an empty argument list" in {
    val givenArguments = List()
    val expectedMessage = "could not format command, no argument provided"

    val producedMessage = JumpAction.posixFormat(givenArguments)
    assert(expectedMessage == producedMessage.left.value)
  }

  it should "handle a single argument" in {
    val givenArguments = List("argument")
    val expectedString = raw"cd 'argument'"

    val producedString = JumpAction.posixFormat(givenArguments)
    assert(expectedString == producedString.right.value)
  }

  it should "handle an argument with an apostrophe" in {
    val givenArguments = List("argu'ment")
    val expectedString = raw"cd 'argu'\''ment'"

    val producedString = JumpAction.posixFormat(givenArguments)
    assert(expectedString == producedString.right.value)
  }

  it should "handle an argument with Unicode" in {
    val givenArguments = List("argument😀")
    val expectedString = raw"cd 'argument😀'"

    val producedString = JumpAction.posixFormat(givenArguments)
    assert(expectedString == producedString.right.value)
  }
}
