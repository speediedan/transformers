# coding=utf-8
# Copyright 2019 HuggingFace Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import shutil
import tempfile
import unittest

from transformers import PreTrainedTokenizerFast
from transformers.testing_utils import require_tokenizers

from .test_tokenization_common import TokenizerTesterMixin


@require_tokenizers
class PreTrainedTokenizationFastTest(TokenizerTesterMixin, unittest.TestCase):
    rust_tokenizer_class = PreTrainedTokenizerFast
    test_slow_tokenizer = False
    test_rust_tokenizer = True
    from_pretrained_vocab_key = "tokenizer_file"

    def setUp(self):
        self.test_rust_tokenizer = False  # because we don't have pretrained_vocab_files_map
        super().setUp()
        self.test_rust_tokenizer = True

        model_paths = ["robot-test/dummy-tokenizer-fast", "robot-test/dummy-tokenizer-wordlevel"]

        # Inclusion of 2 tokenizers to test different types of models (Unigram and WordLevel for the moment)
        self.tokenizers_list = [(PreTrainedTokenizerFast, model_path, {}) for model_path in model_paths]

        tokenizer = PreTrainedTokenizerFast.from_pretrained(model_paths[0])
        tokenizer.save_pretrained(self.tmpdirname)

    def test_pretrained_model_lists(self):
        # We disable this test for PreTrainedTokenizerFast because it is the only tokenizer that is not linked to any
        # model
        pass

    def test_prepare_for_model(self):
        # We disable this test for PreTrainedTokenizerFast because it is the only tokenizer that is not linked to any
        # model
        pass

    def test_rust_tokenizer_signature(self):
        # PreTrainedTokenizerFast doesn't have tokenizer_file in its signature
        pass

    def test_training_new_tokenizer(self):
        tmpdirname_orig = self.tmpdirname
        # Here we want to test the 2 available tokenizers that use 2 different types of models: Unigram and WordLevel.
        for tokenizer, pretrained_name, kwargs in self.tokenizers_list:
            with self.subTest(f"{tokenizer.__class__.__name__} ({pretrained_name})"):
                try:
                    self.tmpdirname = tempfile.mkdtemp()
                    tokenizer = self.rust_tokenizer_class.from_pretrained(pretrained_name, **kwargs)

                    tokenizer.save_pretrained(self.tmpdirname)
                    super().test_training_new_tokenizer()
                finally:
                    # Even if the test fails, we must be sure that the folder is deleted and that the default tokenizer
                    # is restored
                    shutil.rmtree(self.tmpdirname)
                    self.tmpdirname = tmpdirname_orig

    def test_training_new_tokenizer_with_special_tokens_change(self):
        tmpdirname_orig = self.tmpdirname
        # Here we want to test the 2 available tokenizers that use 2 different types of models: Unigram and WordLevel.
        for tokenizer, pretrained_name, kwargs in self.tokenizers_list:
            with self.subTest(f"{tokenizer.__class__.__name__} ({pretrained_name})"):
                try:
                    self.tmpdirname = tempfile.mkdtemp()
                    tokenizer = self.rust_tokenizer_class.from_pretrained(pretrained_name, **kwargs)

                    tokenizer.save_pretrained(self.tmpdirname)
                    super().test_training_new_tokenizer_with_special_tokens_change()
                finally:
                    # Even if the test fails, we must be sure that the folder is deleted and that the default tokenizer
                    # is restored
                    shutil.rmtree(self.tmpdirname)
                    self.tmpdirname = tmpdirname_orig
