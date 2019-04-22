import model.proofreader

def get_model_api():
    """Returns lambda function for api"""

    # 1. initialize model once and for all
    pr = model.proofreader.CNProofReader()


    def model_api(input_data):
        """
        Args:
            input_data: submitted to the API, raw string

        Returns:
            output_data: after some transformation, to be
                returned to the API

        """
        sents = input_data.split('\n')
        html = ""
        for sent in sents:
            details = pr.proofread(sent)

            s = '<div class="e" title="修正候选" data-container="body" \
                data-toggle="popover" data-placement="bottom"  data-html="true" \
                data-content="{0}" > {1} </div>'
    
            last_idx = 0
            for frag, cands in details:
                word, b_idx, e_idx, _ = frag
                data_content = ""
                for cand in cands:
                    data_content += cand + '<br>'

                html += sent[last_idx:b_idx]
                html += s.format(data_content, word)
                last_idx = e_idx
            html += sent[last_idx:]
            html += '<br>'

        return {"input": input_data, "output": html}

    return model_api